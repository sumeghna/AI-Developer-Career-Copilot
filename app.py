# app.py - Complete Version with Interview Questions
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import os
from github import Github
from github.GithubException import GithubException
from datetime import datetime
import random
from dotenv import load_dotenv

# Import from our src modules
from src.github_analyzer import GitHubAnalyzer
from src.skill_extractor import SkillExtractor
from src.career_recommender import CareerRecommender
from src.resume_parser import ResumeParser
from src.job_market import JobMarketAnalyzer
from src.learning_path import LearningPathGenerator
from src.interview_questions import InterviewQuestionGenerator

# Load environment variables from .env file
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Career Copilot",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Modern, Cohesive UI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Animated gradient background for whole app */
    .stApp {
        background: linear-gradient(-45deg, #1a1a2e, #16213e, #0f3460, #1a1a2e);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        min-height: 100vh;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Sidebar styling - matching glass morphism */
    section[data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 10px 0 30px rgba(0, 0, 0, 0.2);
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    
    section[data-testid="stSidebar"] .stRadio > div {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    section[data-testid="stSidebar"] .stRadio label {
        color: white !important;
        font-weight: 500;
        padding: 0.5rem;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    section[data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(255, 255, 255, 0.1);
        transform: translateX(5px);
    }
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label {
        background: rgba(255, 255, 255, 0.05);
        margin: 0.3rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label[data-checked="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border: none;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar input fields */
    section[data-testid="stSidebar"] .stTextInput input {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        color: white;
        padding: 0.8rem 1rem;
        font-size: 1rem;
    }
    
    section[data-testid="stSidebar"] .stTextInput input::placeholder {
        color: rgba(255, 255, 255, 0.5);
    }
    
    section[data-testid="stSidebar"] .stTextInput input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.3);
    }
    
    /* Sidebar buttons */
    section[data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 15px;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    section[data-testid="stSidebar"] .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.5);
    }
    
    /* Sidebar headers */
    section[data-testid="stSidebar"] h2 {
        color: white;
        font-size: 1.8rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    section[data-testid="stSidebar"] h3 {
        color: white;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        opacity: 0.9;
    }
    
    /* Sidebar divider */
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.2);
        margin: 2rem 0;
    }
    
    /* Main content area - glass morphism */
    .main-content {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 30px;
        padding: 2rem;
        margin: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
    }
    
    /* Main header */
    .main-header {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.9), rgba(118, 75, 162, 0.9));
        backdrop-filter: blur(10px);
        padding: 3rem;
        border-radius: 30px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, transparent 70%);
        animation: shine 8s infinite;
    }
    
    @keyframes shine {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .main-header h1 {
        color: white;
        font-size: 3.5rem;
        margin-bottom: 0.5rem;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        letter-spacing: -1px;
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.95);
        font-size: 1.2rem;
        position: relative;
        z-index: 1;
    }
    
    /* Welcome card */
    .welcome-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 3rem;
        border-radius: 40px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 25px 50px rgba(0,0,0,0.3);
        margin: 2rem 0;
    }
    
    .welcome-card h2 {
        background: linear-gradient(135deg, #fff, #e0e0ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
    }
    
    .welcome-card p {
        color: rgba(255,255,255,0.8);
        font-size: 1.2rem;
    }
    
    /* Feature chips */
    .feature-chip {
        display: inline-block;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(5px);
        padding: 0.5rem 1.5rem;
        border-radius: 60px;
        color: white;
        font-weight: 500;
        margin: 0.3rem;
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
    }
    
    .feature-chip:hover {
        background: rgba(102, 126, 234, 0.3);
        transform: translateY(-2px);
    }
    
    /* Feature cards */
    .feature-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 30px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
        height: 100%;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        background: rgba(255, 255, 255, 0.15);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
    }
    
    .feature-card h3 {
        background: linear-gradient(135deg, #fff, #e0e0ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .feature-card p {
        color: rgba(255,255,255,0.8);
        font-size: 1rem;
        line-height: 1.5;
    }
    
    /* Metric cards - consistent styling */
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 25px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
        height: 100%;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.15);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
    }
    
    .metric-card div:first-child {
        color: rgba(255,255,255,0.7);
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    
    .metric-card h3 {
        background: linear-gradient(135deg, #fff, #e0e0ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem !important;
        font-weight: 800;
        margin: 0.3rem 0;
    }
    
    /* Info box */
    .info-box {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 25px;
        margin: 1.5rem 0;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        color: white;
        position: relative;
        overflow: hidden;
    }
    
    .info-box::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 5px;
        height: 100%;
        background: linear-gradient(135deg, #667eea, #764ba2);
    }
    
    .info-box strong {
        color: white;
        font-size: 1.3rem;
        display: block;
        margin-bottom: 1rem;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        padding: 0.8rem;
        border-radius: 60px;
        border: 1px solid rgba(255,255,255,0.2);
        margin-bottom: 2rem;
        flex-wrap: wrap;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        background: transparent;
        padding: 0 1.5rem;
        border-radius: 60px;
        transition: all 0.3s ease;
        color: white !important;
        font-size: 0.9rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stTabs [data-baseweb="tab"] p {
        color: white !important;
        font-weight: 600;
    }
    
    /* Dataframe styling */
    .dataframe {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(5px);
        border-radius: 20px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.2);
        color: white;
    }
    
    .dataframe th {
        background: rgba(102, 126, 234, 0.3);
        color: white;
        font-weight: 600;
        padding: 15px;
    }
    
    .dataframe td {
        color: white;
        padding: 12px 15px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2, #9f7aea);
        background-size: 200% 200%;
        animation: gradient 3s ease infinite;
        border-radius: 10px;
        height: 8px;
    }
    
    /* Repository items */
    .repo-item {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(5px);
        padding: 0.8rem 1.2rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
        color: white;
    }
    
    .repo-item:hover {
        background: rgba(102, 126, 234, 0.3);
        transform: translateX(10px);
    }
    
    /* Complex project items */
    .complex-project {
        background: rgba(102, 126, 234, 0.2);
        backdrop-filter: blur(5px);
        padding: 0.8rem 1.2rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        border-left: 3px solid #667eea;
        transition: all 0.3s ease;
        color: white;
    }
    
    .complex-project:hover {
        transform: translateX(10px);
        background: rgba(102, 126, 234, 0.3);
    }
    
    /* Skill cards */
    .skill-card {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(5px);
        padding: 1.5rem;
        border-radius: 20px;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
        color: white;
    }
    
    .skill-card:hover {
        transform: scale(1.02);
        background: rgba(102, 126, 234, 0.2);
    }
    
    .skill-card span {
        color: white !important;
    }
    
    /* Experience badge */
    .exp-badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        border-radius: 60px;
        font-weight: 700;
        font-size: 1rem;
        margin-right: 0.8rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    .exp-novice { 
        background: linear-gradient(135deg, #64748b, #475569);
        color: white;
    }
    .exp-beginner { 
        background: linear-gradient(135deg, #60a5fa, #3b82f6);
        color: white;
    }
    .exp-intermediate { 
        background: linear-gradient(135deg, #2dd4bf, #14b8a6);
        color: white;
    }
    .exp-advanced { 
        background: linear-gradient(135deg, #c084fc, #a855f7);
        color: white;
    }
    
    /* Course cards for learning path */
    .course-card {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(5px);
        padding: 1.2rem;
        border-radius: 15px;
        margin: 0.8rem 0;
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
    }
    
    .course-card:hover {
        transform: translateX(5px);
        background: rgba(102, 126, 234, 0.2);
        border-left: 3px solid #667eea;
    }
    
    .platform-badge {
        display: inline-block;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    
    .platform-youtube {
        background: #ff0000;
        color: white;
    }
    .platform-udemy {
        background: #a435f0;
        color: white;
    }
    .platform-coursera {
        background: #0056d2;
        color: white;
    }
    .platform-pluralsight {
        background: #f05b2c;
        color: white;
    }
    
    /* Timeline styling */
    .timeline-item {
        display: flex;
        align-items: center;
        margin: 1rem 0;
    }
    
    .timeline-week {
        background: linear-gradient(135deg, #667eea, #764ba2);
        width: 60px;
        height: 60px;
        border-radius: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        margin-right: 1rem;
        flex-shrink: 0;
    }
    
    /* Interview question cards */
    .question-card {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(5px);
        padding: 1.5rem;
        border-radius: 20px;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
    }
    
    .question-card:hover {
        transform: translateX(5px);
        background: rgba(102, 126, 234, 0.15);
    }
    
    .difficulty-badge {
        display: inline-block;
        padding: 0.2rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .difficulty-easy {
        background: #10b981;
        color: white;
    }
    .difficulty-medium {
        background: #f59e0b;
        color: white;
    }
    .difficulty-hard {
        background: #ef4444;
        color: white;
    }
    
    .answer-box {
        background: rgba(0,0,0,0.3);
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
        border-left: 3px solid #667eea;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        background: rgba(0,0,0,0.3);
        backdrop-filter: blur(10px);
        border-radius: 30px;
        border: 1px solid rgba(255,255,255,0.1);
        color: white;
    }
    
    .footer p {
        color: rgba(255,255,255,0.8);
        margin: 0.3rem 0;
    }
    
    /* Error box */
    .error-box {
        background: rgba(229, 62, 62, 0.2);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 20px;
        margin: 1rem 0;
        border: 1px solid #fc8181;
        color: white;
    }
    
    /* Market trend cards */
    .trend-card {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(5px);
        padding: 1.2rem;
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.2);
        margin: 0.5rem 0;
        color: white;
    }
    
    .demand-high {
        color: #4ade80;
        font-weight: 600;
    }
    .demand-medium {
        color: #fbbf24;
        font-weight: 600;
    }
    .demand-low {
        color: #f87171;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# Main content wrapper
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="main-header">
        <h1>🚀 AI Developer Career Copilot</h1>
        <p>Your personalized AI-powered career guidance platform</p>
    </div>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
    st.session_state.skills = []
    st.session_state.proficiency = {}
    st.session_state.languages = {}
    st.session_state.repo_count = 0
    st.session_state.original_repos = 0
    st.session_state.total_commits = 0
    st.session_state.complex_projects = 0
    st.session_state.complex_repo_names = []
    st.session_state.experience_level = "🆕 Novice"
    st.session_state.experience_description = ""
    st.session_state.follower_count = 0
    st.session_state.input_method = None
    st.session_state.input_value = None
    st.session_state.error = None
    st.session_state.user_details = {}
    st.session_state.education = []
    st.session_state.experience_years = 0
    st.session_state.resume_details = {}
    st.session_state.learning_path = None
    st.session_state.target_career = None
    st.session_state.interview_set = None

# Function to analyze GitHub profile
def analyze_github_profile(username):
    """Fetch real data from GitHub API with deep analysis"""
    try:
        token = os.environ.get('GITHUB_TOKEN')
        
        if not token:
            return {"error": "GitHub token not found. Please set the GITHUB_TOKEN environment variable."}
        
        analyzer = GitHubAnalyzer(token)
        
        user_info = analyzer.get_user_info(username)
        if "error" in user_info:
            return {"error": user_info["error"]}
        
        analysis_result = analyzer.analyze_repositories_deep(username)
        if "error" in analysis_result:
            return {"error": analysis_result["error"]}
        
        skill_data = analyzer.extract_skills_with_context(analysis_result)
        
        return {
            "success": True,
            "skills": skill_data["skills"],
            "proficiency": skill_data.get("proficiency", {}),
            "experience_level": skill_data.get("experience_level", "🆕 Novice"),
            "experience_description": skill_data.get("experience_description", ""),
            "languages": analysis_result.get("languages", {}),
            "repo_count": analysis_result.get("total_repos", 0),
            "original_repos": analysis_result.get("original_repos", 0),
            "total_commits": skill_data.get("total_commits", 0),
            "complex_projects": analysis_result.get("complex_projects", 0),
            "complex_repo_names": analysis_result.get("complex_repo_names", []),
            "follower_count": user_info.get("followers", 0),
            "name": user_info.get("name", "N/A"),
            "bio": user_info.get("bio", "N/A"),
            "company": user_info.get("company", "N/A"),
            "location": user_info.get("location", "N/A"),
            "repo_names": [r['name'] for r in analysis_result.get("repos", [])[:5]]
        }
        
    except GithubException as e:
        if e.status == 404:
            return {"error": f"User '{username}' not found on GitHub"}
        elif e.status == 401:
            return {"error": "Invalid GitHub token. Please check your token."}
        elif e.status == 403:
            return {"error": "API rate limit exceeded. Try again later."}
        else:
            return {"error": f"GitHub API error: {str(e)}"}
    except Exception as e:
        return {"error": f"Error: {str(e)}"}

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=80)
    st.markdown("<h2>✨ AI Copilot</h2>", unsafe_allow_html=True)
    
    input_method = st.radio(
        "Choose analysis method:",
        ["🔗 GitHub Profile", "📄 Resume Upload", "✏️ Manual Entry"],
        index=0
    )
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Clean the method name for internal use
    method_map = {
        "🔗 GitHub Profile": "GitHub Profile",
        "📄 Resume Upload": "Resume Upload",
        "✏️ Manual Entry": "Manual Entry"
    }
    selected_method = method_map[input_method]
    
    if selected_method == "GitHub Profile":
        st.markdown("<h3>🔗 GitHub Analysis</h3>", unsafe_allow_html=True)
        github_username = st.text_input("Enter GitHub username:", placeholder="e.g., octocat")
        
        if st.button("🚀 Analyze Profile", use_container_width=True):
            if github_username:
                with st.spinner(f"🔮 Deep analyzing {github_username}..."):
                    result = analyze_github_profile(github_username)
                    
                    if "error" in result:
                        st.session_state.error = result["error"]
                        st.session_state.analysis_done = False
                    else:
                        st.session_state.skills = result["skills"]
                        st.session_state.proficiency = result["proficiency"]
                        st.session_state.languages = result["languages"]
                        st.session_state.repo_count = result["repo_count"]
                        st.session_state.original_repos = result["original_repos"]
                        st.session_state.total_commits = result["total_commits"]
                        st.session_state.complex_projects = result["complex_projects"]
                        st.session_state.complex_repo_names = result.get("complex_repo_names", [])
                        st.session_state.experience_level = result["experience_level"]
                        st.session_state.experience_description = result["experience_description"]
                        st.session_state.follower_count = result["follower_count"]
                        st.session_state.analysis_done = True
                        st.session_state.input_method = "GitHub"
                        st.session_state.input_value = github_username
                        st.session_state.error = None
                        st.session_state.user_details = {
                            "name": result.get("name", "N/A"),
                            "bio": result.get("bio", "N/A"),
                            "company": result.get("company", "N/A"),
                            "location": result.get("location", "N/A"),
                            "repo_names": result.get("repo_names", [])
                        }
                    st.rerun()
            else:
                st.error("⚠️ Enter username")
    
    elif selected_method == "Resume Upload":
        st.markdown("<h3>📄 Resume Upload</h3>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Upload your resume (PDF/DOCX)", 
            type=['pdf', 'docx'],
            help="Upload your resume to extract skills automatically"
        )
        
        if uploaded_file:
            st.success(f"✅ Uploaded: {uploaded_file.name}")
            
            if st.button("📄 Analyze Resume", use_container_width=True):
                with st.spinner("🔍 Parsing resume and extracting skills..."):
                    try:
                        # Import the resume parser
                        from src.resume_parser import ResumeParser
                        
                        # Determine file type
                        file_type = "pdf" if uploaded_file.name.endswith('.pdf') else "docx"
                        
                        # Parse the resume
                        parser = ResumeParser()
                        result = parser.analyze_resume(uploaded_file, file_type)
                        
                        if "error" in result:
                            st.session_state.error = result["error"]
                            st.session_state.analysis_done = False
                        else:
                            # Store results in session state
                            st.session_state.skills = result.get("skills", [])
                            st.session_state.experience_level = result.get("experience_level", "Entry-Level")
                            st.session_state.experience_years = result.get("experience_years", 0)
                            st.session_state.education = result.get("education", [])
                            st.session_state.analysis_done = True
                            st.session_state.input_method = "Resume"
                            st.session_state.input_value = uploaded_file.name
                            st.session_state.error = None
                            
                            # Store additional resume details
                            st.session_state.resume_details = {
                                "has_email": result.get("has_email", False),
                                "has_phone": result.get("has_phone", False),
                                "skill_count": result.get("skill_count", 0)
                            }
                    except Exception as e:
                        st.session_state.error = f"Error parsing resume: {str(e)}"
                        st.session_state.analysis_done = False
                    
                    st.rerun()
    
    else:  # Manual Entry
        st.markdown("<h3>✏️ Manual Entry</h3>", unsafe_allow_html=True)
        manual_skills = st.text_area(
            "List your skills (comma separated):",
            placeholder="e.g., Python, JavaScript, React",
            height=150
        )
        
        if st.button("✨ Analyze Skills", use_container_width=True):
            if manual_skills:
                with st.spinner("✨ Processing..."):
                    time.sleep(1)
                    skills_list = [skill.strip() for skill in manual_skills.split(',')]
                    st.session_state.skills = skills_list[:10]
                    st.session_state.analysis_done = True
                    st.session_state.input_method = "Manual"
                    st.session_state.input_value = f"{len(skills_list)} skills"
                    st.session_state.error = None
                    st.rerun()
            else:
                st.error("⚠️ Enter skills")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; opacity: 0.7; font-size: 0.9rem;'>"
        "Powered by Advanced AI<br>v5.0.0</p>",
        unsafe_allow_html=True
    )

# Main content area
if st.session_state.error:
    st.markdown(f"""
        <div class="error-box">
            <strong>❌ Error</strong><br>
            <span>{st.session_state.error}</span>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 Try Again", use_container_width=True):
            st.session_state.error = None
            st.rerun()

elif not st.session_state.analysis_done:
    # Welcome message
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div class="welcome-card">
                <h2>🚀 Welcome to Your AI Career Copilot</h2>
                <p style="margin-bottom: 2rem;">Unlock your true potential with deep GitHub analysis</p>
                <div style="display: flex; justify-content: center; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 3rem;">
                    <span class="feature-chip">🎯 Smart Matching</span>
                    <span class="feature-chip">📊 Deep Analysis</span>
                    <span class="feature-chip">🚀 Career Paths</span>
                    <span class="feature-chip">📄 Resume Parsing</span>
                    <span class="feature-chip">📈 Market Trends</span>
                    <span class="feature-chip">📚 Learning Paths</span>
                    <span class="feature-chip">🎙️ Interview Prep</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown("""
                <div class="feature-card">
                    <h3>🔗 GitHub</h3>
                    <p>Deep analysis of repositories, commits, and contribution patterns</p>
                </div>
            """, unsafe_allow_html=True)
        with col_b:
            st.markdown("""
                <div class="feature-card">
                    <h3>📄 Resume</h3>
                    <p>Extract and analyze skills from your resume with intelligent parsing</p>
                </div>
            """, unsafe_allow_html=True)
        with col_c:
            st.markdown("""
                <div class="feature-card">
                    <h3>🎙️ Interview</h3>
                    <p>AI-powered interview questions and mock interviews</p>
                </div>
            """, unsafe_allow_html=True)

else:
    # Show analysis results based on input method
    if st.session_state.input_method == "GitHub" and st.session_state.user_details:
        
        # Clean level for badge class (remove emojis)
        exp_level = st.session_state.experience_level.lower()
        clean_level = exp_level.replace("🔥 ", "").replace("📈 ", "").replace("🌱 ", "").replace("🆕 ", "")
        badge_class = f"exp-{clean_level}" if clean_level in ['novice', 'beginner', 'intermediate', 'advanced'] else "exp-beginner"
        
        st.markdown(f"""
            <div class="info-box">
                <strong>✨ GitHub Analysis Complete</strong>
                <div style="display: flex; align-items: center; gap: 1.5rem; margin: 1.5rem 0;">
                    <div style="background: linear-gradient(135deg, #667eea, #764ba2); width: 70px; height: 70px; border-radius: 35px; display: flex; align-items: center; justify-content: center; font-size: 2.5rem;">👤</div>
                    <div>
                        <span style="font-size: 2rem; font-weight: 700; color: white;">{st.session_state.user_details.get('name', 'N/A')}</span><br>
                        <span style="color: rgba(255,255,255,0.7); font-size: 1.1rem;">@{st.session_state.input_value}</span>
                    </div>
                </div>
                <p style="color: rgba(255,255,255,0.8); font-size: 1.1rem; margin: 1rem 0;">{st.session_state.user_details.get('bio', 'No bio provided')}</p>
                <div style="display: flex; gap: 2rem; margin: 1rem 0;">
                    <span>📍 {st.session_state.user_details.get('location', 'N/A')}</span>
                    <span>🏢 {st.session_state.user_details.get('company', 'N/A')}</span>
                </div>
                <div style="margin-top: 1.5rem;">
                    <span class="exp-badge {badge_class}">{st.session_state.experience_level}</span>
                    <span style="color: rgba(255,255,255,0.8);">{st.session_state.experience_description}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Display top repositories
        if st.session_state.user_details.get('repo_names'):
            st.markdown("### 📁 Featured Repositories")
            cols = st.columns(2)
            for i, repo in enumerate(st.session_state.user_details['repo_names']):
                with cols[i % 2]:
                    st.markdown(f"""
                        <div class="repo-item">
                            📂 {repo}
                        </div>
                    """, unsafe_allow_html=True)
        
        # Display complex projects
        if st.session_state.complex_projects > 0:
            st.markdown("### 🏗️ Complex Projects")
            st.markdown(f"<p style='color: rgba(255,255,255,0.8);'>Found {st.session_state.complex_projects} large-scale projects (>1MB) showing depth of experience</p>", unsafe_allow_html=True)
            
            if st.session_state.complex_repo_names:
                cols = st.columns(2)
                for i, repo in enumerate(st.session_state.complex_repo_names[:6]):  # Show up to 6
                    with cols[i % 2]:
                        st.markdown(f"""
                            <div class="complex-project">
                                🚀 {repo}
                            </div>
                        """, unsafe_allow_html=True)
    
    elif st.session_state.input_method == "Resume":
        st.markdown(f"""
            <div class="info-box">
                <strong>✅ Resume Analysis Complete</strong><br>
                <span style="font-size: 1.3rem;">{st.session_state.input_value}</span><br>
                <span style="color: rgba(255,255,255,0.8);">Experience: {st.session_state.experience_level} ({st.session_state.experience_years} years)</span><br>
                <span style="color: rgba(255,255,255,0.8);">Skills Found: {len(st.session_state.skills)}</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Show education if available
        if st.session_state.education:
            st.markdown("### 🎓 Education")
            for edu in st.session_state.education:
                if edu['institution']:
                    st.markdown(f"- **{edu['institution']}**")
                    if edu['details']:
                        st.markdown(f"  {edu['details']}")
    
    else:  # Manual Entry
        st.markdown(f"""
            <div class="info-box">
                <strong>✅ Manual Entry Complete</strong><br>
                <span style="font-size: 1.3rem;">{st.session_state.input_value}</span>
            </div>
        """, unsafe_allow_html=True)
    
    # Tabs for all methods - Now with 6 tabs including Interview Questions
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊 Overview", "🔧 Skills Deep Dive", "🎯 Career Paths", "📈 Market Trends", "📚 Learning Path", "🎙️ Interview Prep"])
    
    with tab1:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div>Skills Detected</div>
                    <h3>{len(st.session_state.skills)}</h3>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            match_count = min(3, len(st.session_state.skills)) if st.session_state.skills else 0
            st.markdown(f"""
                <div class="metric-card">
                    <div>Career Matches</div>
                    <h3>{match_count}</h3>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <div>Experience Level</div>
                    <h3 style="font-size: 2rem;">{st.session_state.experience_level}</h3>
                </div>
            """, unsafe_allow_html=True)
        with col4:
            if st.session_state.input_method == "GitHub":
                if st.session_state.total_commits > 500:
                    activity = "🔥 Very Active"
                elif st.session_state.total_commits > 100:
                    activity = "📈 Active"
                else:
                    activity = "🌱 Growing"
            else:
                activity = "📊 Analyzed"
            st.markdown(f"""
                <div class="metric-card">
                    <div>Activity</div>
                    <h3>{activity}</h3>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Additional stats based on method
        if st.session_state.input_method == "GitHub":
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Repos", st.session_state.repo_count, delta=f"Original: {st.session_state.original_repos}")
            with col2:
                st.metric("Total Commits", f"{st.session_state.total_commits:,}")
            with col3:
                st.metric("Complex Projects", st.session_state.complex_projects)
        
        elif st.session_state.input_method == "Resume":
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Experience Years", st.session_state.experience_years)
            with col2:
                if st.session_state.resume_details:
                    st.metric("Contact Info", "✅ Found" if st.session_state.resume_details.get('has_email') else "⚠️ Missing")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("📋 Skills Overview")
        
        if st.session_state.skills:
            # Create categories properly
            categories_list = ['Language', 'Framework', 'Tool', 'Database', 'Cloud']
            skill_categories = []
            for i in range(len(st.session_state.skills)):
                skill_categories.append(categories_list[i % len(categories_list)])
            
            df = pd.DataFrame({
                'Skill': st.session_state.skills,
                'Category': skill_categories
            })
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Language Distribution Chart (only for GitHub)
            if st.session_state.input_method == "GitHub" and st.session_state.languages:
                st.subheader("📊 Language Distribution")
                lang_df = pd.DataFrame({
                    'Language': list(st.session_state.languages.keys()),
                    'Count': list(st.session_state.languages.values())
                }).sort_values('Count', ascending=False).head(8)
                
                fig = px.bar(
                    lang_df, 
                    x='Language', 
                    y='Count',
                    color='Count',
                    color_continuous_scale=['#667eea', '#9f7aea', '#764ba2'],
                    text='Count'
                )
                
                fig.update_traces(
                    texttemplate='%{text}',
                    textposition='outside',
                    marker_line_width=0,
                    opacity=0.9,
                    textfont_color='white'
                )
                
                fig.update_layout(
                    height=450,
                    xaxis_title="",
                    yaxis_title="Repositories",
                    font=dict(color='white'),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    showlegend=False,
                    xaxis=dict(tickfont=dict(color='white')),
                    yaxis=dict(tickfont=dict(color='white'))
                )
                
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No skills detected")
    
    with tab2:
        st.subheader("🔧 Skill Proficiency Analysis")
        if st.session_state.skills:
            for i, skill in enumerate(st.session_state.skills[:10]):
                if st.session_state.input_method == "GitHub" and skill in st.session_state.proficiency:
                    level = st.session_state.proficiency[skill].get('level', 'Beginner')
                    if level == "Expert":
                        prof = 95
                    elif level == "Intermediate":
                        prof = 75
                    else:
                        prof = 55
                else:
                    prof = 70 + (i * 5) % 25
                
                st.markdown(f"""
                    <div class="skill-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-size: 1.3rem; font-weight: 600;">{skill}</span>
                            <span style="font-size: 1.5rem; font-weight: 700; color: #667eea;">{prof}%</span>
                        </div>
                        <div style="background: rgba(255,255,255,0.2); height: 10px; border-radius: 5px; margin-top: 1rem;">
                            <div style="background: linear-gradient(90deg, #667eea, #764ba2); width: {prof}%; height: 10px; border-radius: 5px;"></div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No skills to display")
    
    with tab3:
        st.subheader("🎯 Career Recommendations")
        recommender = CareerRecommender()
        recommendations = recommender.recommend(st.session_state.skills)
        if recommendations:
            for career in recommendations:
                st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.1); backdrop-filter: blur(5px); padding: 2rem; border-radius: 25px; margin: 1.5rem 0; border: 1px solid rgba(255,255,255,0.2);">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h4 style="color: white; font-size: 1.5rem; font-weight: 700;">{career['title']}</h4>
                            <span style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 0.5rem 1.5rem; border-radius: 60px; font-weight: 700;">{career['match']}% Match</span>
                        </div>
                        <p style="color: #667eea; font-size: 1.2rem; margin: 1rem 0;">💰 {career['salary']}</p>
                        <p style="color: white;"><span style="font-weight: 600;">Required:</span> {', '.join(career['required'])}</p>
                        <p style="color: rgba(255,255,255,0.7);"><span style="font-weight: 600;">Bonus:</span> {', '.join(career['bonus'])}</p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No career matches found. Try adding more skills!")
    
    with tab4:
        st.subheader("📈 Job Market Trends")
        
        # Initialize job market analyzer
        market = JobMarketAnalyzer()
        
        if st.session_state.skills:
            # Get market summary
            summary = market.get_market_summary(st.session_state.skills)
            
            # Display market summary metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Avg. Growth Rate", f"{summary['avg_growth']}%", delta="YoY")
            with col2:
                st.metric("Total Job Openings", f"{summary['total_jobs']:,}")
            with col3:
                st.metric("High Demand Skills", summary['high_demand_count'])
            
            st.markdown(f"### Market Outlook: {summary['outlook']}")
            st.markdown("---")
            
            # Skill trends table
            st.subheader("📊 Skill Demand Trends")
            trends = market.get_skill_trends(st.session_state.skills)
            
            for trend in trends[:8]:
                demand_class = "demand-high" if "High" in trend['demand'] else "demand-medium" if "Stable" in trend['demand'] else "demand-low"
                st.markdown(f"""
                    <div class="trend-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-size: 1.2rem; font-weight: 600;">{trend['skill']}</span>
                            <span class="{demand_class}">{trend['demand']}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-top: 0.5rem;">
                            <span>Growth: {trend['growth']}% YoY</span>
                            <span>{trend['jobs_count']:,} jobs</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Salary comparison for top roles
            st.markdown("---")
            st.subheader("💰 Salary Comparison by Role")
            
            recommender = CareerRecommender()
            top_careers = recommender.recommend(st.session_state.skills)[:3]
            
            if top_careers:
                salary_data = []
                for career in top_careers:
                    role = career['title']
                    salary_prog = market.get_salary_by_experience(role)
                    if salary_prog:
                        salary_data.append({
                            'Role': role,
                            'Entry': salary_prog['entry'],
                            'Mid-Level': salary_prog['mid'],
                            'Senior': salary_prog['senior']
                        })
                
                if salary_data:
                    df_salary = pd.DataFrame(salary_data)
                    fig = go.Figure()
                    
                    for level in ['Entry', 'Mid-Level', 'Senior']:
                        fig.add_trace(go.Bar(
                            name=level,
                            x=df_salary['Role'],
                            y=df_salary[level],
                            text=[f"${x:,.0f}" for x in df_salary[level]],
                            textposition='auto',
                        ))
                    
                    fig.update_layout(
                        barmode='group',
                        height=400,
                        title="Salary Progression by Role",
                        yaxis_title="Annual Salary (USD)",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        legend=dict(font=dict(color='white'))
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No skills to analyze. Please add skills first to see market trends.")
    
    with tab5:
        st.subheader("📚 Personalized Learning Path")
        
        if st.session_state.skills:
            learner = LearningPathGenerator()
            recommender = CareerRecommender()
            top_careers = recommender.recommend(st.session_state.skills)
            
            career_options = [c['title'] for c in top_careers] if top_careers else []
            career_options.append("General Skill Advancement")
            
            selected_career = st.selectbox(
                "🎯 Select your target career:",
                career_options,
                index=0,
                key="learning_path_career"
            )
            
            if st.button("🚀 Generate Learning Path", key="generate_lp", use_container_width=True):
                with st.spinner("Creating personalized learning path..."):
                    target = selected_career if selected_career != "General Skill Advancement" else None
                    learning_path = learner.generate_learning_path(
                        st.session_state.skills, 
                        target,
                        st.session_state.proficiency if st.session_state.input_method == "GitHub" else None
                    )
                    st.session_state.learning_path = learning_path
                    st.session_state.target_career = selected_career
            
            if st.session_state.learning_path:
                lp = st.session_state.learning_path
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Skills to Learn", lp['total_skills'])
                with col2:
                    st.metric("Recommended Courses", lp['total_courses'])
                with col3:
                    st.metric("Est. Duration", f"{lp['estimated_weeks']} weeks")
                
                st.markdown("---")
                
                for item in lp['learning_path']:
                    with st.expander(f"📘 {item['skill']} - Current: {item['current_level'].title()} → Next: {item['next_level'].title()}"):
                        st.markdown(f"**Estimated time:** {item['estimated_hours']} hours")
                        
                        for course in item['recommended_courses']:
                            platform_class = "platform-youtube" if "youtube" in course['url'].lower() or "youtu.be" in course['url'].lower() else \
                                            "platform-udemy" if "udemy" in course['url'].lower() else \
                                            "platform-coursera" if "coursera" in course['url'].lower() else \
                                            "platform-pluralsight" if "pluralsight" in course['url'].lower() else ""
                            
                            st.markdown(f"""
                                <div class="course-card">
                                    <div style="display: flex; justify-content: space-between; align-items: center;">
                                        <span style="font-size: 1.1rem; font-weight: 600;">{course['name']}</span>
                                        <span class="platform-badge {platform_class}">{course['platform']}</span>
                                    </div>
                                    <div style="display: flex; justify-content: space-between; margin-top: 0.5rem;">
                                        <span>⏱️ {course['duration']}</span>
                                        <span>{'🆓 Free' if course.get('free', False) else '💰 Paid'}</span>
                                    </div>
                                    <div style="margin-top: 0.5rem;">
                                        <a href="{course['url']}" target="_blank" style="color: #667eea; text-decoration: none;">🔗 View Course →</a>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                
                st.markdown("---")
                st.subheader("🗓️ Your 8-Week Learning Timeline")
                
                for item in lp['timeline']:
                    st.markdown(f"""
                        <div class="timeline-item">
                            <div class="timeline-week">Week {item['week']}</div>
                            <div style="flex-grow: 1;">
                                <strong style="color: white;">{item['skill']}</strong><br>
                                <span style="color: rgba(255,255,255,0.7);">{item['course']} ({item['platform']})</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
                st.subheader("🆓 Free Resources")
                
                free_resources = []
                for skill in st.session_state.skills[:3]:
                    free_resources.extend(learner.get_free_resources(skill))
                
                if free_resources:
                    for resource in free_resources[:5]:
                        st.markdown(f"""
                            <div class="course-card">
                                <div style="display: flex; justify-content: space-between;">
                                    <span style="font-weight: 600;">{resource['name']}</span>
                                    <span class="platform-badge platform-youtube">FREE</span>
                                </div>
                                <div>
                                    <a href="{resource['url']}" target="_blank" style="color: #667eea;">Watch now →</a>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No free resources found for your skills.")
        else:
            st.info("No skills to analyze. Please add skills first to generate a learning path.")
    
    with tab6:
        st.subheader("🎙️ AI Interview Preparation")
        
        if st.session_state.skills:
            # Initialize interview generator
            interviewer = InterviewQuestionGenerator()
            
            # Experience level selector
            exp_level_options = ["beginner", "intermediate", "senior"]
            selected_exp = st.selectbox(
                "📊 Your Experience Level:",
                exp_level_options,
                index=1,
                key="interview_exp_level"
            )
            
            # Generate interview questions
            if st.button("🎯 Generate Interview Questions", key="generate_interview", use_container_width=True):
                with st.spinner("Generating personalized interview questions..."):
                    interview_set = interviewer.generate_interview_set(
                        st.session_state.skills,
                        selected_exp
                    )
                    st.session_state.interview_set = interview_set
            
            # Display interview set
            if st.session_state.interview_set:
                interview = st.session_state.interview_set
                
                # Stats
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Technical Questions", interview['stats']['technical_count'])
                with col2:
                    st.metric("Behavioral Questions", interview['stats']['behavioral_count'])
                with col3:
                    easy_count = interview['stats']['difficulty_breakdown'].get('easy', 0)
                    medium_count = interview['stats']['difficulty_breakdown'].get('medium', 0)
                    hard_count = interview['stats']['difficulty_breakdown'].get('hard', 0)
                    st.metric("Difficulty", f"E:{easy_count} M:{medium_count} H:{hard_count}")
                
                st.markdown("---")
                
                # Technical Questions Section
                st.subheader("💻 Technical Questions")
                for i, q in enumerate(interview['technical_questions'][:5], 1):
                    diff_class = f"difficulty-{q.get('difficulty', 'medium')}"
                    st.markdown(f"""
                        <div class="question-card">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="font-size: 1.1rem; font-weight: 600;">Q{i}. {q['question']}</span>
                                <span class="difficulty-badge {diff_class}">{q.get('difficulty', 'medium').upper()}</span>
                            </div>
                            <div style="margin-top: 0.5rem;">
                                <span style="color: rgba(255,255,255,0.7); font-size: 0.9rem;">Skill: {q['skill']} • Level: {q['level']}</span>
                            </div>
                            <div style="margin-top: 0.8rem;">
                                <details>
                                    <summary style="color: #667eea; cursor: pointer;">📖 View Answer</summary>
                                    <div class="answer-box">
                                        <strong>Answer:</strong> {q.get('answer', 'Use STAR method to structure your answer.')}
                                        <br><br>
                                        <strong>Tips:</strong>
                                        <ul>
                                            {''.join([f'<li>{tip}</li>' for tip in q.get('tips', [])])}
                                        </ul>
                                    </div>
                                </details>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Behavioral Questions Section
                st.subheader("🤝 Behavioral Questions")
                for i, q in enumerate(interview['behavioral_questions'][:3], 1):
                    st.markdown(f"""
                        <div class="question-card">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="font-size: 1.1rem; font-weight: 600;">B{i}. {q['question']}</span>
                                <span class="difficulty-badge difficulty-medium">BEHAVIORAL</span>
                            </div>
                            <div style="margin-top: 0.8rem;">
                                <details>
                                    <summary style="color: #667eea; cursor: pointer;">💡 Tips</summary>
                                    <div class="answer-box">
                                        <strong>Tips:</strong>
                                        <ul>
                                            {''.join([f'<li>{tip}</li>' for tip in q.get('tips', ['Use STAR method', 'Be specific', 'Show impact'])])}
                                        </ul>
                                    </div>
                                </details>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Tips Section
                st.subheader("💡 Interview Tips")
                tips_cols = st.columns(2)
                for i, tip in enumerate(interview['tips']):
                    with tips_cols[i % 2]:
                        st.markdown(f"✅ {tip}")
                
                # Mock Interview Button
                st.markdown("---")
                if st.button("🎭 Start Mock Interview", key="mock_interview", use_container_width=True):
                    mock = interviewer.get_mock_interview(st.session_state.skills)
                    st.session_state.mock_interview = mock
                
                if st.session_state.get('mock_interview'):
                    mock = st.session_state.mock_interview
                    st.success(f"🎤 Mock Interview Session ({mock['duration_minutes']} minutes)")
                    
                    for section in mock['sections']:
                        st.markdown(f"""
                            <div style="background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 15px; margin: 1rem 0;">
                                <h4 style="color: #667eea;">{section['name']} ({section['duration']} min)</h4>
                                <p>{section.get('prompt', '')}</p>
                                {' '.join([f'<p>• {q["question"]}</p>' for q in section.get('questions', [])]) if section.get('questions') else ''}
                            </div>
                        """, unsafe_allow_html=True)
        else:
            st.info("No skills to analyze. Please add skills first to generate interview questions.")
    
    # Reset button
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("🔄 New Analysis", use_container_width=True):
            st.session_state.analysis_done = False
            st.session_state.skills = []
            st.session_state.languages = {}
            st.session_state.error = None
            st.session_state.education = []
            st.session_state.complex_repo_names = []
            st.session_state.learning_path = None
            st.session_state.interview_set = None
            st.rerun()

# Footer
st.markdown("""
    <div class="footer">
        <p style="font-size: 1.2rem; font-weight: 600;">🚀 AI Developer Career Copilot</p>
        <p style="font-size: 1rem; opacity: 0.8;">Deep GitHub analysis • Intelligent resume parsing • Real-time market trends • Personalized learning paths • AI interview preparation</p>
        <p style="font-size: 0.9rem; opacity: 0.6; margin-top: 1rem;">© 2025 • Powered by Advanced AI</p>
    </div>
""", unsafe_allow_html=True)

# Close main content wrapper
st.markdown('</div>', unsafe_allow_html=True)