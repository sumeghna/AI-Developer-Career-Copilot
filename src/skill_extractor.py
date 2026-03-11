# src/skill_extractor.py
import re

class SkillExtractor:
    def __init__(self):
        self.common_skills = [
            "Python", "JavaScript", "Java", "C++", "Ruby", "PHP", "Swift", "Kotlin",
            "React", "Angular", "Vue", "Django", "Flask", "Spring", "Express",
            "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Git",
            "SQL", "MongoDB", "PostgreSQL", "MySQL", "Redis",
            "HTML", "CSS", "TypeScript", "Node.js", "GraphQL"
        ]
    
    def extract_from_text(self, text):
        """Extract skills from text"""
        found_skills = []
        text_lower = text.lower()
        
        for skill in self.common_skills:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        return found_skills
    
    def extract_from_github_data(self, github_data):
        """Extract skills from GitHub analysis data"""
        if "skills" in github_data:
            return github_data["skills"]
        return []