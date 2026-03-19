# src/job_market.py
import requests
import json
import random
from datetime import datetime
from typing import Dict, List, Any

class JobMarketAnalyzer:
    def __init__(self):
        self.salary_data = self._load_salary_data()
        self.trend_data = self._load_trend_data()
        
    def _load_salary_data(self) -> Dict:
        """Load salary data by role and location"""
        return {
            "Full Stack Developer": {
                "entry": {"US": 75000, "UK": 45000, "India": 800000, "Canada": 65000, "Germany": 55000},
                "mid": {"US": 105000, "UK": 65000, "India": 1500000, "Canada": 90000, "Germany": 75000},
                "senior": {"US": 145000, "UK": 90000, "India": 2500000, "Canada": 130000, "Germany": 95000}
            },
            "Frontend Developer": {
                "entry": {"US": 70000, "UK": 42000, "India": 700000, "Canada": 60000, "Germany": 50000},
                "mid": {"US": 95000, "UK": 60000, "India": 1300000, "Canada": 85000, "Germany": 70000},
                "senior": {"US": 130000, "UK": 80000, "India": 2200000, "Canada": 120000, "Germany": 90000}
            },
            "Backend Developer": {
                "entry": {"US": 80000, "UK": 48000, "India": 900000, "Canada": 70000, "Germany": 60000},
                "mid": {"US": 110000, "UK": 70000, "India": 1600000, "Canada": 95000, "Germany": 80000},
                "senior": {"US": 150000, "UK": 95000, "India": 2800000, "Canada": 140000, "Germany": 100000}
            },
            "DevOps Engineer": {
                "entry": {"US": 85000, "UK": 50000, "India": 1000000, "Canada": 75000, "Germany": 65000},
                "mid": {"US": 120000, "UK": 75000, "India": 1800000, "Canada": 105000, "Germany": 85000},
                "senior": {"US": 160000, "UK": 100000, "India": 3000000, "Canada": 150000, "Germany": 110000}
            },
            "Data Engineer": {
                "entry": {"US": 90000, "UK": 52000, "India": 1100000, "Canada": 80000, "Germany": 70000},
                "mid": {"US": 125000, "UK": 78000, "India": 2000000, "Canada": 115000, "Germany": 90000},
                "senior": {"US": 165000, "UK": 105000, "India": 3500000, "Canada": 160000, "Germany": 120000}
            },
            "Python Developer": {
                "entry": {"US": 78000, "UK": 45000, "India": 850000, "Canada": 68000, "Germany": 58000},
                "mid": {"US": 108000, "UK": 68000, "India": 1550000, "Canada": 95000, "Germany": 78000},
                "senior": {"US": 148000, "UK": 92000, "India": 2700000, "Canada": 135000, "Germany": 98000}
            },
            "Java Developer": {
                "entry": {"US": 76000, "UK": 44000, "India": 820000, "Canada": 66000, "Germany": 56000},
                "mid": {"US": 104000, "UK": 65000, "India": 1450000, "Canada": 92000, "Germany": 75000},
                "senior": {"US": 142000, "UK": 88000, "India": 2600000, "Canada": 130000, "Germany": 95000}
            }
        }
    
    def _load_trend_data(self) -> Dict:
        """Load market trend data"""
        return {
            "Python": {"demand": "🔥 Very High", "growth": 25, "jobs_count": 45000},
            "JavaScript": {"demand": "🔥 Very High", "growth": 20, "jobs_count": 52000},
            "React": {"demand": "🔥 Very High", "growth": 30, "jobs_count": 38000},
            "TypeScript": {"demand": "📈 High", "growth": 35, "jobs_count": 28000},
            "Node.js": {"demand": "📈 High", "growth": 22, "jobs_count": 32000},
            "Docker": {"demand": "📈 High", "growth": 28, "jobs_count": 25000},
            "Kubernetes": {"demand": "🚀 Emerging", "growth": 45, "jobs_count": 15000},
            "AWS": {"demand": "🔥 Very High", "growth": 32, "jobs_count": 42000},
            "Azure": {"demand": "📈 High", "growth": 25, "jobs_count": 28000},
            "GCP": {"demand": "📈 High", "growth": 30, "jobs_count": 18000},
            "SQL": {"demand": "📊 Stable", "growth": 5, "jobs_count": 35000},
            "MongoDB": {"demand": "📈 High", "growth": 18, "jobs_count": 20000},
            "PostgreSQL": {"demand": "📈 High", "growth": 15, "jobs_count": 22000},
            "Java": {"demand": "📊 Stable", "growth": 8, "jobs_count": 38000},
            "Go": {"demand": "🚀 Emerging", "growth": 40, "jobs_count": 16000},
            "Rust": {"demand": "🚀 Emerging", "growth": 50, "jobs_count": 8000},
            "GraphQL": {"demand": "📈 High", "growth": 35, "jobs_count": 14000}
        }
    
    def get_salary_for_role(self, role: str, level: str = "mid", location: str = "US") -> Dict:
        """Get salary data for a specific role"""
        if role in self.salary_data:
            if level in self.salary_data[role]:
                if location in self.salary_data[role][level]:
                    salary = self.salary_data[role][level][location]
                    currency = "$" if location in ["US", "Canada"] else "£" if location == "UK" else "€" if location in ["Germany"] else "₹"
                    return {
                        "role": role,
                        "level": level,
                        "location": location,
                        "salary": salary,
                        "currency": currency,
                        "formatted": f"{currency}{salary:,}"
                    }
        return {"error": "Data not found"}
    
    def get_skill_trends(self, skills: List[str]) -> List[Dict]:
        """Get market trends for given skills"""
        trends = []
        for skill in skills:
            if skill in self.trend_data:
                trends.append({
                    "skill": skill,
                    **self.trend_data[skill]
                })
            else:
                trends.append({
                    "skill": skill,
                    "demand": "📊 Stable",
                    "growth": random.randint(5, 15),
                    "jobs_count": random.randint(5000, 20000)
                })
        return sorted(trends, key=lambda x: x["growth"], reverse=True)
    
    def get_top_locations_for_role(self, role: str) -> List[Dict]:
        """Get top locations for a role"""
        locations = []
        if role in self.salary_data:
            for location in ["US", "UK", "India", "Canada", "Germany"]:
                if location in self.salary_data[role]["mid"]:
                    locations.append({
                        "location": location,
                        "avg_salary": self.salary_data[role]["mid"][location]
                    })
        return sorted(locations, key=lambda x: x["avg_salary"], reverse=True)
    
    def get_market_summary(self, skills: List[str]) -> Dict:
        """Get overall market summary based on skills"""
        trends = self.get_skill_trends(skills)
        
        if not trends:
            return {"error": "No skills provided"}
        
        avg_growth = sum(t["growth"] for t in trends) / len(trends)
        total_jobs = sum(t["jobs_count"] for t in trends)
        high_demand_count = sum(1 for t in trends if "High" in t["demand"] or "Very High" in t["demand"])
        
        if avg_growth > 30:
            outlook = "🚀 Excellent - High growth field"
        elif avg_growth > 20:
            outlook = "📈 Good - Growing field"
        elif avg_growth > 10:
            outlook = "📊 Stable - Moderate growth"
        else:
            outlook = "⚠️ Mature - Slow growth"
        
        return {
            "avg_growth": round(avg_growth, 1),
            "total_jobs": total_jobs,
            "high_demand_count": high_demand_count,
            "outlook": outlook,
            "trending_skills": trends[:3]
        }
    
    def get_salary_by_experience(self, role: str) -> Dict:
        """Get salary progression by experience"""
        if role in self.salary_data:
            return {
                "entry": self.salary_data[role]["entry"]["US"],
                "mid": self.salary_data[role]["mid"]["US"],
                "senior": self.salary_data[role]["senior"]["US"]
            }
        return {}