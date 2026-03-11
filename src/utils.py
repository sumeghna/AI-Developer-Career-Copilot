# src/utils.py
import json
import os

def load_skills_database():
    """Load skills database from JSON file"""
    try:
        with open('data/skills_database.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"programming_languages": [], "frameworks": [], "databases": [], "devops_tools": []}

def format_skills_for_display(skills):
    """Format skills for display in UI"""
    if not skills:
        return "No skills found"
    return ", ".join(skills[:10])