# src/career_recommender.py
class CareerRecommender:
    def __init__(self):
        self.career_paths = {
            "Python Developer": {
                "required": ["Python"],
                "bonus": ["Django", "Flask", "SQL"],
                "salary": "$80k-120k"
            },
            "Frontend Developer": {
                "required": ["JavaScript", "React"],
                "bonus": ["TypeScript", "HTML", "CSS"],
                "salary": "$75k-115k"
            },
            "Java Developer": {
                "required": ["Java"],
                "bonus": ["Spring", "SQL"],
                "salary": "$85k-125k"
            },
            "DevOps Engineer": {
                "required": ["Docker", "AWS"],
                "bonus": ["Kubernetes", "Jenkins"],
                "salary": "$95k-140k"
            },
            "Full Stack Developer": {
                "required": ["Python", "JavaScript", "React", "SQL"],
                "bonus": ["Node.js", "MongoDB"],
                "salary": "$85k-130k"
            }
        }
    
    def recommend(self, skills):
        """Recommend careers based on skills"""
        recommendations = []
        
        for career, details in self.career_paths.items():
            # Calculate match score
            required_matches = sum(1 for skill in details["required"] if skill in skills)
            bonus_matches = sum(1 for skill in details["bonus"] if skill in skills)
            
            required_total = len(details["required"])
            if required_total > 0:
                match_score = (required_matches / required_total * 70) + (bonus_matches * 5)
                match_score = min(100, int(match_score))
                
                if match_score > 30:  # Only show if at least 30% match
                    recommendations.append({
                        "title": career,
                        "match": match_score,
                        "salary": details["salary"],
                        "required": details["required"],
                        "bonus": details["bonus"]
                    })
        
        # Sort by match score descending
        recommendations.sort(key=lambda x: x["match"], reverse=True)
        return recommendations[:3]