# src/learning_path.py
import json
import random
from typing import List, Dict, Any
import requests
from datetime import datetime

class LearningPathGenerator:
    def __init__(self):
        self.courses_db = self._load_courses()
        self.youtube_api_key = None  # You can add YouTube API key later
        
    def _load_courses(self) -> Dict:
        """Load courses database"""
        return {
            "Python": {
                "beginner": [
                    {"name": "Python for Beginners", "platform": "YouTube", "url": "https://youtu.be/_uQrJ0TkZlc", "duration": "4 hours", "free": True},
                    {"name": "Complete Python Bootcamp", "platform": "Udemy", "url": "https://www.udemy.com/course/python-complete-bootcamp/", "duration": "20 hours", "free": False},
                    {"name": "Python Basics", "platform": "Coursera", "url": "https://www.coursera.org/learn/python", "duration": "15 hours", "free": True}
                ],
                "intermediate": [
                    {"name": "Python OOP", "platform": "YouTube", "url": "https://youtu.be/Ej_02ICOIgs", "duration": "3 hours", "free": True},
                    {"name": "Python Data Structures", "platform": "Coursera", "url": "https://www.coursera.org/learn/python-data", "duration": "20 hours", "free": True},
                    {"name": "Advanced Python", "platform": "Udemy", "url": "https://www.udemy.com/course/advanced-python/", "duration": "15 hours", "free": False}
                ],
                "advanced": [
                    {"name": "Python Design Patterns", "platform": "YouTube", "url": "https://youtu.be/bsyjSW46TDg", "duration": "2 hours", "free": True},
                    {"name": "Python Concurrency", "platform": "Pluralsight", "url": "https://www.pluralsight.com/courses/python-concurrency", "duration": "4 hours", "free": False}
                ]
            },
            "JavaScript": {
                "beginner": [
                    {"name": "JavaScript for Beginners", "platform": "YouTube", "url": "https://youtu.be/W6NZfCO5SIk", "duration": "3 hours", "free": True},
                    {"name": "The Complete JavaScript Course", "platform": "Udemy", "url": "https://www.udemy.com/course/the-complete-javascript-course/", "duration": "30 hours", "free": False}
                ],
                "intermediate": [
                    {"name": "JavaScript: The Weird Parts", "platform": "YouTube", "url": "https://youtu.be/Bv_5Zv5c-Ts", "duration": "2 hours", "free": True},
                    {"name": "Modern JavaScript", "platform": "Coursera", "url": "https://www.coursera.org/learn/javascript", "duration": "15 hours", "free": True}
                ],
                "advanced": [
                    {"name": "Advanced JavaScript", "platform": "Pluralsight", "url": "https://www.pluralsight.com/courses/advanced-javascript", "duration": "5 hours", "free": False}
                ]
            },
            "React": {
                "beginner": [
                    {"name": "React for Beginners", "platform": "YouTube", "url": "https://youtu.be/Ke90Tje7VS0", "duration": "2 hours", "free": True},
                    {"name": "Modern React with Redux", "platform": "Udemy", "url": "https://www.udemy.com/course/react-redux/", "duration": "40 hours", "free": False}
                ],
                "intermediate": [
                    {"name": "React Hooks", "platform": "YouTube", "url": "https://youtu.be/mxK8b99iJTg", "duration": "1 hour", "free": True},
                    {"name": "Advanced React Patterns", "platform": "FrontendMasters", "url": "https://frontendmasters.com/courses/advanced-react-patterns/", "duration": "5 hours", "free": False}
                ],
                "advanced": [
                    {"name": "React Performance", "platform": "YouTube", "url": "https://youtu.be/5fLW5Q5ODiE", "duration": "1 hour", "free": True}
                ]
            },
            "Django": {
                "beginner": [
                    {"name": "Django for Beginners", "platform": "YouTube", "url": "https://youtu.be/F5mRW0jo-U4", "duration": "2 hours", "free": True},
                    {"name": "Python Django Web Framework", "platform": "Coursera", "url": "https://www.coursera.org/learn/django", "duration": "20 hours", "free": True}
                ],
                "intermediate": [
                    {"name": "Django REST Framework", "platform": "YouTube", "url": "https://youtu.be/cJveik3w9dM", "duration": "2 hours", "free": True}
                ],
                "advanced": [
                    {"name": "Django Advanced Topics", "platform": "Udemy", "url": "https://www.udemy.com/course/advanced-django/", "duration": "10 hours", "free": False}
                ]
            },
            "Docker": {
                "beginner": [
                    {"name": "Docker for Beginners", "platform": "YouTube", "url": "https://youtu.be/3c-iBn73dDE", "duration": "1 hour", "free": True},
                    {"name": "Docker Mastery", "platform": "Udemy", "url": "https://www.udemy.com/course/docker-mastery/", "duration": "20 hours", "free": False}
                ],
                "intermediate": [
                    {"name": "Docker Compose", "platform": "YouTube", "url": "https://youtu.be/Qw9zlE3t8Ko", "duration": "1 hour", "free": True}
                ],
                "advanced": [
                    {"name": "Docker in Production", "platform": "Pluralsight", "url": "https://www.pluralsight.com/courses/docker-production", "duration": "3 hours", "free": False}
                ]
            },
            "AWS": {
                "beginner": [
                    {"name": "AWS for Beginners", "platform": "YouTube", "url": "https://youtu.be/3hLmDS179YE", "duration": "2 hours", "free": True},
                    {"name": "AWS Certified Cloud Practitioner", "platform": "Udemy", "url": "https://www.udemy.com/course/aws-certified-cloud-practitioner/", "duration": "15 hours", "free": False}
                ],
                "intermediate": [
                    {"name": "AWS Solutions Architect", "platform": "Coursera", "url": "https://www.coursera.org/learn/aws-solutions-architect", "duration": "30 hours", "free": True}
                ]
            },
            "SQL": {
                "beginner": [
                    {"name": "SQL for Beginners", "platform": "YouTube", "url": "https://youtu.be/7S_tz1z_5bA", "duration": "3 hours", "free": True},
                    {"name": "SQL Bootcamp", "platform": "Udemy", "url": "https://www.udemy.com/course/sql-bootcamp/", "duration": "10 hours", "free": False}
                ],
                "intermediate": [
                    {"name": "Advanced SQL", "platform": "YouTube", "url": "https://youtu.be/2-1XQHAgDsM", "duration": "2 hours", "free": True}
                ]
            }
        }
    
    def get_skill_level(self, skill: str, current_skills: List[str], proficiency: Dict = None) -> str:
        """Determine user's level for a specific skill"""
        if proficiency and skill in proficiency:
            return proficiency[skill].get('level', 'beginner').lower()
        return "beginner"  # Default to beginner if not found
    
    def generate_learning_path(self, current_skills: List[str], target_career: str = None, proficiency: Dict = None) -> Dict[str, Any]:
        """Generate personalized learning path"""
        
        # Determine which skills to learn based on target career or skill gaps
        skills_to_learn = []
        
        if target_career:
            # Career-specific skill recommendations
            career_skills = {
                "Full Stack Developer": ["React", "Node.js", "Python", "SQL", "Docker"],
                "Python Developer": ["Python", "Django", "SQL", "Docker"],
                "Frontend Developer": ["JavaScript", "React", "HTML", "CSS"],
                "DevOps Engineer": ["Docker", "AWS", "Python", "Kubernetes"],
                "Data Engineer": ["Python", "SQL", "AWS", "Docker"]
            }
            
            recommended = career_skills.get(target_career, [])
            skills_to_learn = [s for s in recommended if s not in current_skills]
        else:
            # If no target career, recommend advanced levels of current skills
            for skill in current_skills[:3]:  # Top 3 skills
                if skill in self.courses_db:
                    skills_to_learn.append(skill)
        
        # Generate learning path for each skill
        learning_path = []
        total_duration = 0
        
        for skill in skills_to_learn[:3]:  # Limit to 3 skills
            if skill in self.courses_db:
                level = self.get_skill_level(skill, current_skills, proficiency)
                
                # Get courses for this skill at appropriate level
                skill_courses = []
                if level == "beginner":
                    skill_courses = self.courses_db[skill].get("beginner", [])
                elif level == "intermediate":
                    skill_courses = self.courses_db[skill].get("intermediate", [])
                    # Also recommend some beginner if needed
                    skill_courses.extend(self.courses_db[skill].get("beginner", [])[:1])
                else:  # advanced
                    skill_courses = self.courses_db[skill].get("advanced", [])
                    skill_courses.extend(self.courses_db[skill].get("intermediate", [])[:1])
                
                # Calculate total duration
                for course in skill_courses:
                    try:
                        hours = int(''.join(filter(str.isdigit, course.get('duration', '0'))))
                        total_duration += hours
                    except:
                        pass
                
                learning_path.append({
                    "skill": skill,
                    "current_level": level,
                    "recommended_courses": skill_courses[:3],  # Top 3 courses
                    "estimated_hours": sum([int(''.join(filter(str.isdigit, c.get('duration', '0')))) for c in skill_courses[:3] if c.get('duration')]),
                    "next_level": "intermediate" if level == "beginner" else "advanced" if level == "intermediate" else "expert"
                })
        
        # Create roadmap timeline
        timeline = []
        weeks = 1
        for item in learning_path:
            for course in item['recommended_courses']:
                timeline.append({
                    "week": weeks,
                    "skill": item['skill'],
                    "course": course['name'],
                    "platform": course['platform'],
                    "duration": course['duration'],
                    "url": course['url']
                })
                weeks += 1
        
        return {
            "learning_path": learning_path,
            "timeline": timeline[:8],  # First 8 weeks
            "total_skills": len(learning_path),
            "total_courses": len(timeline),
            "total_duration_hours": total_duration,
            "estimated_weeks": len(timeline),
            "target_career": target_career
        }
    
    def get_free_resources(self, skill: str) -> List[Dict]:
        """Get free learning resources for a skill"""
        free_resources = []
        if skill in self.courses_db:
            for level in ['beginner', 'intermediate', 'advanced']:
                for course in self.courses_db[skill].get(level, []):
                    if course.get('free', False):
                        free_resources.append(course)
        return free_resources[:5]
    
    def get_certification_path(self, skill: str) -> List[Dict]:
        """Get certification recommendations"""
        certs = {
            "Python": [
                {"name": "PCAP - Certified Associate Python Programmer", "provider": "Python Institute", "url": "https://pythoninstitute.org/pcap"},
                {"name": "PCEP - Certified Entry-Level Python Programmer", "provider": "Python Institute", "url": "https://pythoninstitute.org/pcep"}
            ],
            "AWS": [
                {"name": "AWS Certified Cloud Practitioner", "provider": "Amazon", "url": "https://aws.amazon.com/certification/certified-cloud-practitioner/"},
                {"name": "AWS Solutions Architect Associate", "provider": "Amazon", "url": "https://aws.amazon.com/certification/certified-solutions-architect-associate/"}
            ],
            "Docker": [
                {"name": "Docker Certified Associate", "provider": "Docker", "url": "https://training.mirantis.com/certification/"}
            ]
        }
        return certs.get(skill, [])