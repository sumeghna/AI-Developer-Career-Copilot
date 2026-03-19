# src/github_analyzer.py - Fixed to get ALL repositories and track complex projects
from github import Github
from github.GithubException import GithubException
import time

class GitHubAnalyzer:
    def __init__(self, token):
        self.token = token
        self.g = Github(token)
    
    def get_user_info(self, username):
        """Get basic user information"""
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
                'created_at': user.created_at,
                'updated_at': user.updated_at
            }
        except GithubException as e:
            return {"error": str(e)}
    
    def get_all_repos(self, username):
        """Get ALL repositories (handles pagination)"""
        try:
            user = self.g.get_user(username)
            all_repos = []
            
            # Get all repositories (this handles pagination automatically)
            repos = user.get_repos()
            
            # Convert to list to get all items
            for repo in repos:
                all_repos.append(repo)
            
            print(f"✅ Found total {len(all_repos)} repositories for {username}")
            return all_repos
            
        except GithubException as e:
            print(f"❌ Error getting repos: {e}")
            return []
    
    def analyze_repositories_deep(self, username):
        """Deep analysis of repositories to determine actual skill level"""
        try:
            # Get ALL repositories
            all_repos = self.get_all_repos(username)
            
            repos_data = []
            total_commits = 0
            total_prs = 0
            total_issues = 0
            complex_projects = 0
            complex_repo_names = []  # Track complex repo names
            languages = {}
            original_repos_count = 0
            fork_count = 0
            
            for repo in all_repos:
                # Count forks vs originals
                if repo.fork:
                    fork_count += 1
                    continue  # Skip forked repos for skill analysis
                
                original_repos_count += 1
                
                # Get languages used in this repo
                repo_languages = repo.get_languages()
                for lang, bytes_count in repo_languages.items():
                    if lang in languages:
                        languages[lang] += 1
                    else:
                        languages[lang] = 1
                
                # Analyze repo complexity
                repo_data = {
                    'name': repo.name,
                    'description': repo.description,
                    'language': repo.language,
                    'stars': repo.stargazers_count,
                    'forks': repo.forks_count,
                    'size': repo.size,  # Size in KB
                    'has_wiki': repo.has_wiki,
                    'has_pages': repo.has_pages,
                    'created_at': repo.created_at,
                    'updated_at': repo.updated_at,
                    'is_fork': repo.fork
                }
                
                # Check for complexity indicators (large projects)
                if repo.size > 1000:  # Large project (>1MB)
                    complex_projects += 1
                    complex_repo_names.append(repo.name)  # Track complex repo name
                
                # Get commit count (approximate)
                try:
                    commits = repo.get_commits().totalCount
                    repo_data['commit_count'] = commits
                    total_commits += commits
                except:
                    repo_data['commit_count'] = 0
                
                repos_data.append(repo_data)
            
            # Calculate experience level based on multiple factors
            experience_score = 0
            
            # Factor 1: Number of original repos (not forks)
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
            
            # Factor 4: Stars received (community recognition)
            total_stars = sum(r.get('stars', 0) for r in repos_data)
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
            
            return {
                "repos": repos_data[:10],  # Top 10 repos for display
                "languages": languages,
                "total_repos": len(all_repos),
                "original_repos": original_repos_count,
                "forked_repos": fork_count,
                "complex_projects": complex_projects,
                "complex_repo_names": complex_repo_names[:5],  # Top 5 complex repos
                "total_commits": total_commits,
                "total_stars": total_stars,
                "experience_score": experience_score,
                "level": level,
                "level_description": level_description
            }
            
        except GithubException as e:
            return {"error": str(e)}
    
    def extract_skills_with_context(self, analysis_result):
        """Extract skills with context about proficiency"""
        skills = []
        skill_proficiency = {}
        
        # Add languages with context
        for lang, count in analysis_result.get('languages', {}).items():
            # More repos in a language = higher proficiency
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