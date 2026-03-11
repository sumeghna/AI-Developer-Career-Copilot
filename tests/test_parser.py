# test_parser.py
from src.resume_parser import ResumeParser

parser = ResumeParser()
print("✅ Resume Parser loaded successfully!")
print(f"Skills database size: {len(parser.skills_database)}")