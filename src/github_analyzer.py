# src/github_analyzer.py - Optimized with parallel processing and caching
import json
import os
from github import Github
from github.GithubException import GithubException
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

class GitHubAnalyzer:
    def __init__(self, token):
        self.token = token
        self.g = Github(token)
        self.cache_file = "data/github_cache.json"
        self.cache_duration = timedelta(hours=24)  # Cache for 24 hours
        self.executor = ThreadPoolExecutor(max_workers=10)  # Parallel processing
    
    def _get_cached_result(self, username):
        """Get cached analysis result if not expired"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    cache = json.load(f)
                    if username in cache:
                        cached_time = datetime.fromisoformat(cache[username]['timestamp'])
                        if datetime.now() - cached_time < self.cache_duration:
                            print(f"✅ Using cached data for {username}")
                            return cache[username]['data']
        except Exception as e:
            print(f"Cache read error: {e}")
        return None
    
    def _cache_result(self, username, data):
        """Save analysis result to cache"""
        try:
            cache = {}
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    cache = json.load(f)
            
            cache[username] = {
                'timestamp': datetime.now().isoformat(),
                'data': data
            }
            
            # Keep only last 50 users in cache
            if len(cache) > 50:
                # Remove oldest entries
                sorted_items = sorted(cache.items(), 
                                     key=lambda x: x[1]['timestamp'])
                for i in range(len(cache) - 50):
                    del cache[sorted_items[i][0]]
            
            with open(self.cache_file, 'w') as f:
                json.dump(cache, f)
        except Exception as e:
            print(f"Cache write error: {e}")
    
    def get_user_info(self, username):
        """Get basic user information (sync, fast)"""
        try:
            user = self.g.get_user(username)
            return {
                'name': user.name,
                'login': user.login,
                'public_repos': user.public_repos,
                'followers': user.followers,
                'following': user.following,
                'bio': user.bio,
                'company': user.company,
                'location': user.location,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'updated_at': user.updated_at.isoformat() if user.updated_at else None
            }
        except GithubException as e:
            return {"error": str(e)}
    
    def get_all_repos_parallel(self, username, progress_callback=None):
        """Get ALL repositories using parallel processing"""
        try:
            user = self.g.get_user(username)
            
            # Get all repositories
            repos = user.get_repos()
            all_repos = list(repos)
            
            total_repos = len(all_repos)
            if progress_callback:
                progress_callback("fetching", 0, total_repos)
            
            # Process repos in parallel
            repo_data_list = []
            completed = 0
            
            # Use ThreadPoolExecutor for parallel API calls
            def process_repo(repo):
                if repo.fork:
                    return None
                
                # Get languages (fast API call)
                try:
                    repo_languages = repo.get_languages()
                except:
                    repo_languages = {}
                
                # Get commit count (just the count, not all commits)
                try:
                    commits = repo.get_commits().totalCount
                except:
                    commits = 0
                
                return {
                    'name': repo.name,
                    'description': repo.description,
                    'language': repo.language,
                    'stars': repo.stargazers_count,
                    'forks': repo.forks_count,
                    'size': repo.size,
                    'is_fork': repo.fork,
                    'languages': repo_languages,
                    'commit_count': commits,
                    'created_at': repo.created_at.isoformat() if repo.created_at else None,
                    'updated_at': repo.updated_at.isoformat() if repo.updated_at else None
                }
            
            # Process repos in parallel with progress
            with ThreadPoolExecutor(max_workers=10) as executor:
                future_to_repo = {executor.submit(process_repo, repo): repo for repo in all_repos}
                
                for future in as_completed(future_to_repo):
                    result = future.result()
                    if result:
                        repo_data_list.append(result)
                    completed += 1
                    if progress_callback:
                        progress_callback("processing", completed, total_repos)
            
            return repo_data_list, total_repos
            
        except GithubException as e:
            print(f"Error getting repos: {e}")
            return [], 0
    
    def analyze_repositories_deep(self, username, progress_callback=None):
        """Deep analysis with parallel processing and caching"""
        try:
            # Check cache first
            cached = self._get_cached_result(username)
            if cached:
                return cached
            
            # Get all repos with parallel processing
            if progress_callback:
                progress_callback("fetching_repos", 0, 100)
            
            repo_data_list, total_repos = self.get_all_repos_parallel(username, progress_callback)
            
            # Analyze data
            languages = {}
            original_repos_count = 0
            fork_count = 0
            complex_projects = 0
            complex_repo_names = []
            total_commits = 0
            total_stars = 0
            
            for repo_data in repo_data_list:
                original_repos_count += 1
                
                # Languages
                for lang, count in repo_data.get('languages', {}).items():
                    if lang in languages:
                        languages[lang] += 1
                    else:
                        languages[lang] = 1
                
                # Complex projects (size > 1MB)
                if repo_data.get('size', 0) > 1000:
                    complex_projects += 1
                    complex_repo_names.append(repo_data['name'])
                
                total_commits += repo_data.get('commit_count', 0)
                total_stars += repo_data.get('stars', 0)
            
            fork_count = total_repos - original_repos_count
            
            # Calculate experience score
            experience_score = 0
            
            # Factor 1: Original repos
            if original_repos_count > 20:
                experience_score += 40
            elif original_repos_count > 10:
                experience_score += 30
            elif original_repos_count > 5:
                experience_score += 20
            elif original_repos_count > 2:
                experience_score += 10
            
            # Factor 2: Complex projects
            if complex_projects > 10:
                experience_score += 30
            elif complex_projects > 5:
                experience_score += 25
            elif complex_projects > 2:
                experience_score += 15
            elif complex_projects > 0:
                experience_score += 5
            
            # Factor 3: Total commits
            if total_commits > 1000:
                experience_score += 30
            elif total_commits > 500:
                experience_score += 25
            elif total_commits > 200:
                experience_score += 15
            elif total_commits > 50:
                experience_score += 10
            
            # Factor 4: Stars received
            if total_stars > 500:
                experience_score += 15
            elif total_stars > 100:
                experience_score += 10
            elif total_stars > 10:
                experience_score += 5
            
            # Determine level with emoji indicators
            if experience_score >= 80:
                level = "🔥 Advanced"
                level_description = f"Experienced developer with {original_repos_count} original projects and {total_commits:,}+ commits"
            elif experience_score >= 50:
                level = "📈 Intermediate"
                level_description = f"Growing developer with {original_repos_count} original projects and consistent contributions"
            elif experience_score >= 20:
                level = "🌱 Beginner"
                level_description = f"Early career developer with {original_repos_count} projects, building experience"
            else:
                level = "🆕 Novice"
                level_description = f"Just starting with {original_repos_count} projects"
            
            result = {
                "repos": repo_data_list[:10],  # Top 10 repos for display
                "languages": languages,
                "total_repos": total_repos,
                "original_repos": original_repos_count,
                "forked_repos": fork_count,
                "complex_projects": complex_projects,
                "complex_repo_names": complex_repo_names[:5],
                "total_commits": total_commits,
                "total_stars": total_stars,
                "experience_score": experience_score,
                "level": level,
                "level_description": level_description
            }
            
            # Cache the result
            self._cache_result(username, result)
            
            return result
            
        except Exception as e:
            return {"error": str(e)}
    
    def extract_skills_with_context(self, analysis_result):
        """Extract skills with context about proficiency"""
        skills = []
        skill_proficiency = {}
        
        # Add languages with context
        for lang, count in analysis_result.get('languages', {}).items():
            if count >= 8:
                proficiency = "Expert"
            elif count >= 4:
                proficiency = "Intermediate"
            else:
                proficiency = "Beginner"
            
            skills.append(lang)
            skill_proficiency[lang] = {
                "level": proficiency,
                "repos_using": count
            }
        
        # Add frameworks based on languages and project complexity
        if "JavaScript" in skills or "TypeScript" in skills:
            if analysis_result.get('complex_projects', 0) > 3:
                skills.extend(["React", "Node.js", "Express", "Vue"])
            elif analysis_result.get('complex_projects', 0) > 1:
                skills.extend(["React", "Node.js"])
            else:
                skills.extend(["React"])
        
        if "Python" in skills:
            if analysis_result.get('complex_projects', 0) > 3:
                skills.extend(["Django", "Flask", "FastAPI", "Pandas"])
            elif analysis_result.get('complex_projects', 0) > 1:
                skills.extend(["Django", "Flask"])
            else:
                skills.extend(["Django"])
        
        if "Java" in skills:
            if analysis_result.get('complex_projects', 0) > 2:
                skills.extend(["Spring", "Hibernate", "Maven"])
            else:
                skills.append("Spring")
        
        if "Go" in skills:
            if analysis_result.get('complex_projects', 0) > 1:
                skills.extend(["Docker", "Kubernetes"])
            else:
                skills.append("Docker")
        
        if "Ruby" in skills:
            skills.append("Rails")
        
        if "PHP" in skills:
            skills.append("Laravel")
        
        if "HTML" in skills or "CSS" in skills:
            skills.append("Frontend Development")
        
        # Remove duplicates while preserving order
        seen = set()
        unique_skills = []
        for skill in skills:
            if skill not in seen:
                seen.add(skill)
                unique_skills.append(skill)
        
        return {
            "skills": unique_skills[:15],
            "proficiency": skill_proficiency,
            "experience_level": analysis_result.get('level', '🆕 Novice'),
            "experience_description": analysis_result.get('level_description', ''),
            "total_commits": analysis_result.get('total_commits', 0),
            "original_projects": analysis_result.get('original_repos', 0),
            "forked_projects": analysis_result.get('forked_repos', 0)
        }