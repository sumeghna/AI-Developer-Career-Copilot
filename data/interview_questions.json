# src/interview_questions.py
import json
import random
from typing import List, Dict, Any
from datetime import datetime

class InterviewQuestionGenerator:
    def __init__(self):
        self.questions_db = self._load_questions()
        
    def _load_questions(self) -> Dict:
        """Load interview questions database"""
        return {
            "Python": {
                "beginner": [
                    {
                        "question": "What is Python? What are its key features?",
                        "answer": "Python is a high-level, interpreted programming language known for its simplicity and readability. Key features include dynamic typing, garbage collection, extensive standard library, and support for multiple programming paradigms.",
                        "tips": ["Mention that it's interpreted", "Talk about indentation", "Discuss OOP support"],
                        "difficulty": "easy"
                    },
                    {
                        "question": "Explain the difference between lists and tuples in Python.",
                        "answer": "Lists are mutable (can be changed) while tuples are immutable (cannot be changed). Lists use [] brackets, tuples use () brackets. Tuples are faster for iteration.",
                        "tips": ["Give examples", "Memory efficiency of tuples", "When to use each"],
                        "difficulty": "easy"
                    },
                    {
                        "question": "What are Python decorators?",
                        "answer": "Decorators are functions that modify the behavior of other functions. They take a function as input, add some functionality, and return a new function. Used with @ syntax.",
                        "tips": ["Explain with @ symbol", "Give real-world example like @app.route in Flask", "Mention they're wrappers"],
                        "difficulty": "medium"
                    },
                    {
                        "question": "Explain the Global Interpreter Lock (GIL) in Python.",
                        "answer": "GIL is a mutex that allows only one thread to execute Python bytecode at a time. This simplifies memory management but limits multi-threading performance. Use multiprocessing for CPU-bound tasks.",
                        "tips": ["Mention it's in CPython", "Discuss alternatives like Jython", "When to use threading vs multiprocessing"],
                        "difficulty": "hard"
                    }
                ],
                "intermediate": [
                    {
                        "question": "What are metaclasses in Python?",
                        "answer": "Metaclasses are classes of classes. They define how a class behaves. A class is an instance of a metaclass. type is the built-in metaclass.",
                        "tips": ["Explain that classes are objects too", "Use cases like ORMs", "Mention __new__ and __init__"],
                        "difficulty": "hard"
                    },
                    {
                        "question": "Explain context managers and the 'with' statement.",
                        "answer": "Context managers allow you to allocate and release resources precisely. Using 'with' ensures that resources are properly cleaned up after use, even if exceptions occur. Implement using __enter__ and __exit__ methods.",
                        "tips": ["Give file handling example", "Mention contextlib module", "Custom context managers"],
                        "difficulty": "medium"
                    }
                ],
                "advanced": [
                    {
                        "question": "How would you implement a singleton pattern in Python?",
                        "answer": "Several ways: using __new__ method, using decorators, using metaclasses, or using modules (which are naturally singletons in Python).",
                        "tips": ["Show multiple implementations", "Discuss thread safety", "When singletons are useful"],
                        "difficulty": "hard"
                    },
                    {
                        "question": "Explain Python's method resolution order (MRO).",
                        "answer": "MRO is the order in which Python looks for methods in class hierarchies. It uses C3 linearization algorithm. Can be viewed using .__mro__ attribute.",
                        "tips": ["Diamond problem", "super() usage", "C3 algorithm basics"],
                        "difficulty": "hard"
                    }
                ]
            },
            "JavaScript": {
                "beginner": [
                    {
                        "question": "What is JavaScript and where is it used?",
                        "answer": "JavaScript is a high-level, interpreted programming language primarily used for web development. It runs in browsers to create interactive websites and can also run on servers using Node.js.",
                        "tips": ["Mention it's not Java", "Talk about client-side vs server-side", "ES6+ features"],
                        "difficulty": "easy"
                    },
                    {
                        "question": "Explain the difference between let, const, and var.",
                        "answer": "var is function-scoped and can be redeclared. let and const are block-scoped. const cannot be reassigned, but its properties can be modified.",
                        "tips": ["Hoisting differences", "Temporal dead zone", "Best practices"],
                        "difficulty": "easy"
                    },
                    {
                        "question": "What are closures in JavaScript?",
                        "answer": "A closure is a function that has access to its outer function's scope even after the outer function has returned. They're created every time a function is created.",
                        "tips": ["Give counter example", "Data privacy", "Event handlers"],
                        "difficulty": "medium"
                    }
                ],
                "intermediate": [
                    {
                        "question": "What is the difference between == and ===?",
                        "answer": "== checks for value equality after type coercion. === checks for both value and type equality (strict equality). Always use === to avoid unexpected type conversions.",
                        "tips": ["Coercion rules", "Falsy values", "Best practices"],
                        "difficulty": "easy"
                    },
                    {
                        "question": "Explain promises and async/await.",
                        "answer": "Promises represent eventual completion of async operations. async/await is syntactic sugar over promises, making async code look synchronous.",
                        "tips": ["Promise states", "Error handling with try/catch", "Promise chaining"],
                        "difficulty": "medium"
                    }
                ]
            },
            "React": {
                "beginner": [
                    {
                        "question": "What is React and what are its main features?",
                        "answer": "React is a JavaScript library for building user interfaces. Main features: virtual DOM, component-based architecture, JSX, unidirectional data flow, and hooks.",
                        "tips": ["Compare with other frameworks", "Explain component lifecycle", "Virtual DOM benefits"],
                        "difficulty": "easy"
                    },
                    {
                        "question": "Explain the difference between state and props.",
                        "answer": "Props are read-only data passed from parent to child components. State is mutable data managed within a component. Changes in state trigger re-renders.",
                        "tips": ["Lifting state up", "Prop drilling", "When to use each"],
                        "difficulty": "easy"
                    }
                ],
                "intermediate": [
                    {
                        "question": "What are React hooks?",
                        "answer": "Hooks are functions that allow functional components to use state and lifecycle features. Common hooks: useState, useEffect, useContext, useReducer, useMemo, useCallback.",
                        "tips": ["Rules of hooks", "Custom hooks", "Hooks vs classes"],
                        "difficulty": "medium"
                    }
                ]
            },
            "Django": {
                "beginner": [
                    {
                        "question": "What is Django and its architecture?",
                        "answer": "Django is a high-level Python web framework that follows MVT (Model-View-Template) architecture. It emphasizes reusability and 'batteries-included' philosophy.",
                        "tips": ["Compare with MVC", "Discuss ORM", "Admin interface"],
                        "difficulty": "easy"
                    }
                ]
            },
            "Docker": {
                "beginner": [
                    {
                        "question": "What is Docker and why is it used?",
                        "answer": "Docker is a platform for developing, shipping, and running applications in containers. Containers are lightweight, portable, and ensure consistency across environments.",
                        "tips": ["Containers vs VMs", "Dockerfile", "Images and containers"],
                        "difficulty": "easy"
                    }
                ]
            },
            "SQL": {
                "beginner": [
                    {
                        "question": "What is SQL and what are its main types of commands?",
                        "answer": "SQL is a language for managing relational databases. Main command types: DDL (CREATE, ALTER, DROP), DML (SELECT, INSERT, UPDATE, DELETE), DCL (GRANT, REVOKE), TCL (COMMIT, ROLLBACK).",
                        "tips": ["Give examples", "Explain each category", "Use cases"],
                        "difficulty": "easy"
                    },
                    {
                        "question": "Explain different types of JOINs in SQL.",
                        "answer": "INNER JOIN: returns matching records from both tables. LEFT JOIN: all from left, matching from right. RIGHT JOIN: all from right, matching from left. FULL JOIN: all records from both tables.",
                        "tips": ["Venn diagram explanation", "Performance considerations", "Use cases"],
                        "difficulty": "medium"
                    }
                ]
            },
            "General": {
                "behavioral": [
                    {
                        "question": "Tell me about a challenging project you worked on.",
                        "answer": "This is your chance to showcase problem-solving skills. Use STAR method: Situation, Task, Action, Result.",
                        "tips": ["Be specific", "Highlight your role", "Mention technologies used", "Discuss lessons learned"],
                        "difficulty": "medium"
                    },
                    {
                        "question": "How do you stay updated with new technologies?",
                        "answer": "I follow tech blogs, participate in online courses, contribute to open source, attend meetups/conferences, and build side projects.",
                        "tips": ["Be honest", "Show enthusiasm", "Mention specific resources"],
                        "difficulty": "easy"
                    },
                    {
                        "question": "Describe a time you had a conflict with a teammate.",
                        "answer": "Use STAR method. Focus on communication, compromise, and positive outcome.",
                        "tips": ["Stay professional", "Show emotional intelligence", "Emphasize resolution"],
                        "difficulty": "medium"
                    },
                    {
                        "question": "Where do you see yourself in 5 years?",
                        "answer": "Discuss career goals aligned with the role. Show ambition but realism.",
                        "tips": ["Be honest", "Show growth mindset", "Relate to company"],
                        "difficulty": "easy"
                    }
                ]
            }
        }
    
    def get_questions_by_skill(self, skill: str, level: str = "beginner", count: int = 3) -> List[Dict]:
        """Get interview questions for a specific skill and level"""
        questions = []
        
        # Check if skill exists
        if skill in self.questions_db:
            if level in self.questions_db[skill]:
                questions = self.questions_db[skill][level]
        
        # If not enough questions, get from other levels
        if len(questions) < count:
            for lvl in ["beginner", "intermediate", "advanced"]:
                if lvl != level and lvl in self.questions_db.get(skill, {}):
                    questions.extend(self.questions_db[skill][lvl])
        
        # Add some behavioral questions
        if "General" in self.questions_db and "behavioral" in self.questions_db["General"]:
            behavioral = self.questions_db["General"]["behavioral"]
            questions.extend(behavioral[:1])
        
        # Remove duplicates and limit
        unique_questions = []
        seen = set()
        for q in questions:
            if q['question'] not in seen:
                seen.add(q['question'])
                unique_questions.append(q)
        
        return unique_questions[:count]
    
    def generate_interview_set(self, skills: List[str], experience_level: str = "beginner") -> Dict[str, Any]:
        """Generate a complete interview question set based on user's skills"""
        
        interview_set = {
            "technical_questions": [],
            "behavioral_questions": [],
            "system_design": [],
            "tips": []
        }
        
        # Get technical questions for top skills
        for skill in skills[:3]:  # Top 3 skills
            skill_level = "beginner"
            if experience_level.lower() in ["senior", "advanced"]:
                skill_level = "advanced"
            elif experience_level.lower() in ["intermediate", "mid-level"]:
                skill_level = "intermediate"
            
            questions = self.get_questions_by_skill(skill, skill_level, 2)
            interview_set["technical_questions"].extend([
                {
                    "skill": skill,
                    "level": skill_level,
                    **q
                } for q in questions
            ])
        
        # Add behavioral questions
        if "General" in self.questions_db and "behavioral" in self.questions_db["General"]:
            interview_set["behavioral_questions"] = random.sample(
                self.questions_db["General"]["behavioral"], 
                min(3, len(self.questions_db["General"]["behavioral"]))
            )
        
        # Add general tips
        interview_set["tips"] = [
            "Research the company before the interview",
            "Prepare examples using STAR method",
            "Review fundamental concepts in your top skills",
            "Prepare questions to ask the interviewer",
            "Practice coding on a whiteboard or paper"
        ]
        
        # Calculate difficulty distribution
        difficulty_count = {"easy": 0, "medium": 0, "hard": 0}
        for q in interview_set["technical_questions"]:
            diff = q.get('difficulty', 'medium')
            difficulty_count[diff] = difficulty_count.get(diff, 0) + 1
        
        interview_set["stats"] = {
            "total_questions": len(interview_set["technical_questions"]) + len(interview_set["behavioral_questions"]),
            "technical_count": len(interview_set["technical_questions"]),
            "behavioral_count": len(interview_set["behavioral_questions"]),
            "difficulty_breakdown": difficulty_count
        }
        
        return interview_set
    
    def get_mock_interview(self, skills: List[str]) -> Dict[str, Any]:
        """Generate a mock interview session"""
        
        interview = self.generate_interview_set(skills)
        
        # Add mock interview structure
        mock_session = {
            "duration_minutes": 45,
            "sections": [
                {
                    "name": "Introduction",
                    "duration": 5,
                    "prompt": "Tell me about yourself and your background."
                },
                {
                    "name": "Technical Questions",
                    "duration": 25,
                    "questions": interview["technical_questions"][:3]
                },
                {
                    "name": "Behavioral Questions",
                    "duration": 10,
                    "questions": interview["behavioral_questions"][:2]
                },
                {
                    "name": "Your Questions",
                    "duration": 5,
                    "prompt": "Do you have any questions for us?"
                }
            ],
            "tips": interview["tips"]
        }
        
        return mock_session
    
    def get_answer_help(self, question: str) -> Dict[str, str]:
        """Get help for answering a specific question"""
        # Search for the question in database
        for skill, levels in self.questions_db.items():
            for level, questions in levels.items():
                for q in questions:
                    if q['question'].lower() in question.lower() or question.lower() in q['question'].lower():
                        return {
                            "answer": q.get('answer', ''),
                            "tips": q.get('tips', []),
                            "difficulty": q.get('difficulty', 'medium')
                        }
        
        return {
            "answer": "Use the STAR method (Situation, Task, Action, Result) to structure your answer.",
            "tips": ["Be specific", "Quantify results", "Show impact"],
            "difficulty": "medium"
        }