# src/github_analyzer.py - Enhanced Version
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
    
    def analyze_repositories_deep(self, username):
        """Deep analysis of repositories to determine actual skill level"""
        try:
            user = self.g.get_user(username)
            repos_data = []
            total_commits = 0
            total_prs = 0
            total_issues = 0
            complex_projects = 0
            languages = {}
            
            for repo in user.get_repos():
                # Skip forked repos (they don't represent original work)
                if repo.fork:
                    continue
                
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
                
                # Check for complexity indicators
                if repo.size > 1000:  # Large project (>1MB)
                    complex_projects += 1
                
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
            original_repos = len([r for r in repos_data if not r.get('is_fork', False)])
            if original_repos > 10:
                experience_score += 30
            elif original_repos > 5:
                experience_score += 20
            elif original_repos > 2:
                experience_score += 10
            
            # Factor 2: Complex projects
            if complex_projects > 5:
                experience_score += 30
            elif complex_projects > 2:
                experience_score += 20
            elif complex_projects > 0:
                experience_score += 10
            
            # Factor 3: Total commits
            if total_commits > 500:
                experience_score += 30
            elif total_commits > 200:
                experience_score += 20
            elif total_commits > 50:
                experience_score += 10
            
            # Factor 4: Stars received (community recognition)
            total_stars = sum(r.get('stars', 0) for r in repos_data)
            if total_stars > 100:
                experience_score += 10
            elif total_stars > 10:
                experience_score += 5
            
            # Determine level
            if experience_score >= 70:
                level = "Advanced"
                level_description = "Experienced developer with substantial project history"
            elif experience_score >= 40:
                level = "Intermediate"
                level_description = "Growing developer with solid project experience"
            elif experience_score >= 10:
                level = "Beginner"
                level_description = "Early career developer building foundation"
            else:
                level = "Novice"
                level_description = "Just starting their coding journey"
            
            return {
                "repos": repos_data[:10],  # Top 10 repos
                "languages": languages,
                "total_repos": len(repos_data),
                "original_repos": original_repos,
                "complex_projects": complex_projects,
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
            if count >= 5:
                proficiency = "Expert"
            elif count >= 3:
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
            if analysis_result.get('complex_projects', 0) > 2:
                skills.extend(["React", "Node.js", "Express"])
            else:
                skills.extend(["React", "Node.js"])
        
        if "Python" in skills:
            if analysis_result.get('complex_projects', 0) > 2:
                skills.extend(["Django", "Flask", "FastAPI"])
            else:
                skills.extend(["Django", "Flask"])
        
        # Remove duplicates
        seen = set()
        unique_skills = []
        for skill in skills:
            if skill not in seen:
                seen.add(skill)
                unique_skills.append(skill)
        
        return {
            "skills": unique_skills[:15],
            "proficiency": skill_proficiency,
            "experience_level": analysis_result.get('level', 'Beginner'),
            "experience_description": analysis_result.get('level_description', ''),
            "total_commits": analysis_result.get('total_commits', 0),
            "original_projects": analysis_result.get('original_repos', 0)
        }