# src/resume_parser.py
import PyPDF2
import docx
import re
import spacy
from typing import List, Dict, Any

class ResumeParser:
    def __init__(self):
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")
        
        # Common skills database
        self.skills_database = [
            "Python", "JavaScript", "Java", "C++", "C#", "Ruby", "PHP", "Swift", "Kotlin",
            "React", "Angular", "Vue", "Django", "Flask", "Spring", "Express", "Node.js",
            "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Git", "Jenkins",
            "SQL", "MongoDB", "PostgreSQL", "MySQL", "Redis",
            "HTML", "CSS", "TypeScript", "GraphQL",
            "TensorFlow", "PyTorch", "Pandas", "NumPy",
            "Agile", "Scrum", "Jira"
        ]
        
        # Education keywords
        self.education_keywords = [
            "bachelor", "master", "phd", "b.tech", "m.tech", "b.e.", "m.e.",
            "computer science", "information technology", "engineering",
            "university", "college", "institute"
        ]
    
    def extract_text_from_pdf(self, pdf_file) -> str:
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            return f"Error reading PDF: {str(e)}"
    
    def extract_text_from_docx(self, docx_file) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(docx_file)
            text = ""
            for para in doc.paragraphs:
                text += para.text + "\n"
            return text
        except Exception as e:
            return f"Error reading DOCX: {str(e)}"
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from text"""
        found_skills = []
        text_lower = text.lower()
        
        for skill in self.skills_database:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        return list(set(found_skills))[:15]
    
    def extract_education(self, text: str) -> List[Dict[str, str]]:
        """Extract education information"""
        education = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in self.education_keywords):
                education.append({
                    "institution": line.strip(),
                    "details": lines[i+1].strip() if i+1 < len(lines) else ""
                })
        
        return education[:3]
    
    def extract_experience_years(self, text: str) -> int:
        """Extract years of experience"""
        patterns = [
            r'(\d+)[\+]?\s*years?\s*(?:of)?\s*experience',
            r'experience\s*(?:of)?\s*(\d+)[\+]?\s*years?'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                return int(match.group(1))
        
        return 0
    
    def analyze_resume(self, file, file_type: str) -> Dict[str, Any]:
        """Main method to analyze resume"""
        # Extract text
        if file_type == "pdf":
            text = self.extract_text_from_pdf(file)
        elif file_type == "docx":
            text = self.extract_text_from_docx(file)
        else:
            return {"error": "Unsupported file type"}
        
        if "Error" in text:
            return {"error": text}
        
        # Extract information
        skills = self.extract_skills(text)
        education = self.extract_education(text)
        experience_years = self.extract_experience_years(text)
        
        # Determine level
        if experience_years >= 5:
            level = "Senior"
        elif experience_years >= 2:
            level = "Mid-Level"
        else:
            level = "Entry-Level"
        
        return {
            "success": True,
            "skills": skills,
            "skill_count": len(skills),
            "education": education,
            "experience_years": experience_years,
            "experience_level": level,
            "has_email": bool(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)),
            "has_phone": bool(re.search(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', text))
        }