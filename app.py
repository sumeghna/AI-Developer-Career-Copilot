# app.py - MAIN FULL UI VERSION
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import random

# Page configuration - MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="AI Career Copilot",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    /* Main header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .main-header h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.95;
    }
    
    /* Card styling */
    .skill-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 0.5rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    .skill-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
    }
    .metric-card h3 {
        color: #667eea;
        font-size: 2rem;
        margin: 0.5rem 0;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #667eea, #764ba2);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea20 0%, #764ba220 100%);
        border-radius: 15px;
        margin-top: 3rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
    <div class="main-header">
        <h1>🚀 AI Developer Career Copilot</h1>
        <p>Your personalized AI-powered career guidance platform</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar for input
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=80)
    st.markdown("<h2 style='color: white; text-align: center;'>Input Options</h2>", 
                unsafe_allow_html=True)
    
    input_method = st.radio(
        "Choose analysis method:",
        ["GitHub Profile", "Resume Upload", "Manual Entry"],
        index=0
    )
    
    if input_method == "GitHub Profile":
        github_username = st.text_input("Enter GitHub username:", placeholder="e.g., octocat")
        analyze_btn = st.button("🔍 Analyze GitHub Profile", use_container_width=True)
        
    elif input_method == "Resume Upload":
        uploaded_file = st.file_uploader(
            "Upload your resume (PDF/DOCX)", 
            type=['pdf', 'docx'],
            help="Upload your resume to extract skills automatically"
        )
        if uploaded_file:
            st.success(f"✅ Uploaded: {uploaded_file.name}")
        analyze_btn = st.button("📄 Analyze Resume", use_container_width=True)
        
    else:
        st.info("Enter your skills manually")
        manual_skills = st.text_area(
            "List your skills (comma separated):",
            placeholder="Python, JavaScript, React, Docker..."
        )
        analyze_btn = st.button("✨ Analyze Skills", use_container_width=True)
    
    st.markdown("---")
    st.markdown(
        "<p style='color: white; text-align: center; font-size: 0.9rem;'>"
        "Powered by AI • v1.0.0</p>",
        unsafe_allow_html=True
    )

# Main content area
if 'analyze_btn' in locals() and analyze_btn:
    with st.spinner("🔮 Analyzing your profile... This may take a moment."):
        # Progress bar animation
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Simulate analysis steps
        steps = [
            "Fetching GitHub data...",
            "Analyzing repositories...",
            "Extracting skills...",
            "Matching with career database...",
            "Generating recommendations..."
        ]
        
        for i, step in enumerate(steps):
            status_text.text(f"Step {i+1}/5: {step}")
            for j in range(20):
                progress_bar.progress(i*20 + j + 1)
                import time
                time.sleep(0.01)
        
        status_text.text("✅ Analysis complete!")
        time.sleep(0.5)
        status_text.empty()
        progress_bar.empty()
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🔧 Skills", "🎯 Careers", "📈 Roadmap"])
    
    with tab1:
        # Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
                <div class="metric-card">
                    <div>🎯 Skills Detected</div>
                    <h3>24</h3>
                    <div style='color: #4CAF50;'>↑ +5 new</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class="metric-card">
                    <div>💼 Career Matches</div>
                    <h3>8</h3>
                    <div style='color: #4CAF50;'>3 top matches</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
                <div class="metric-card">
                    <div>⭐ Experience Level</div>
                    <h3>Intermediate</h3>
                    <div>3-5 years</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
                <div class="metric-card">
                    <div>📊 Market Demand</div>
                    <h3>High</h3>
                    <div style='color: #4CAF50;'>↑ +15%</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Skill Distribution Chart
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.subheader("📊 Skill Distribution")
            
            # Sample data for demonstration
            skills_df = pd.DataFrame({
                'Category': ['Languages', 'Frameworks', 'Databases', 'DevOps', 'Frontend'],
                'Count': [8, 6, 3, 4, 3]
            })
            
            fig = px.pie(
                skills_df, 
                values='Count', 
                names='Category',
                color_discrete_sequence=px.colors.sequential.Purples_r,
                hole=0.4
            )
            fig.update_layout(
                showlegend=True,
                height=400,
                margin=dict(t=0, b=0, l=0, r=0)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🔥 Hot Skills")
            
            hot_skills = [
                ("Python", 95),
                ("React", 88),
                ("TypeScript", 82),
                ("Docker", 78),
                ("AWS", 75),
                ("GraphQL", 70)
            ]
            
            for skill, demand in hot_skills:
                st.markdown(f"""
                    <div style="margin: 10px 0;">
                        <div style="display: flex; justify-content: space-between;">
                            <span>{skill}</span>
                            <span>{demand}%</span>
                        </div>
                        <div style="background: #e0e0e0; height: 8px; border-radius: 4px;">
                            <div style="background: linear-gradient(90deg, #667eea, #764ba2); 
                                      width: {demand}%; height: 8px; border-radius: 4px;"></div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.subheader("🔧 Your Skills Analysis")
        
        # Skill categories
        categories = ['Programming Languages', 'Frameworks', 'Databases', 'DevOps Tools', 'Frontend']
        
        for category in categories:
            with st.expander(f"📁 {category}", expanded=True):
                col1, col2, col3 = st.columns(3)
                
                # Sample skills
                skills_sample = {
                    'Programming Languages': ['Python', 'JavaScript', 'TypeScript', 'Java', 'Go'],
                    'Frameworks': ['React', 'Django', 'Flask', 'Express', 'Spring'],
                    'Databases': ['PostgreSQL', 'MongoDB', 'Redis', 'MySQL'],
                    'DevOps Tools': ['Docker', 'Kubernetes', 'Jenkins', 'AWS', 'GitHub Actions'],
                    'Frontend': ['HTML5', 'CSS3', 'Tailwind', 'Bootstrap', 'Material-UI']
                }
                
                skills = skills_sample.get(category, [])
                for i, skill in enumerate(skills):
                    with col1 if i % 3 == 0 else col2 if i % 3 == 1 else col3:
                        proficiency = random.randint(60, 95)
                        st.markdown(f"""
                            <div class="skill-card">
                                <h4>{skill}</h4>
                                <div style="margin-top: 10px;">
                                    <div style="background: #e0e0e0; height: 6px; border-radius: 3px;">
                                        <div style="background: linear-gradient(90deg, #667eea, #764ba2); 
                                                  width: {proficiency}%; height: 6px; border-radius: 3px;"></div>
                                    </div>
                                    <p style="margin-top: 5px;">Proficiency: {proficiency}%</p>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
    
    with tab3:
        st.subheader("🎯 Career Matches")
        
        # Career matches
        careers = [
            {
                "title": "Full Stack Developer",
                "match": 92,
                "salary": "$85k - $120k",
                "demand": "High",
                "skills_match": ["✅ Python", "✅ React", "✅ SQL", "❌ TypeScript", "❌ GraphQL"],
                "color": "#667eea"
            },
            {
                "title": "Data Engineer",
                "match": 87,
                "salary": "$95k - $135k",
                "demand": "Very High",
                "skills_match": ["✅ Python", "✅ SQL", "✅ Pandas", "❌ Spark", "❌ Airflow"],
                "color": "#764ba2"
            },
            {
                "title": "DevOps Engineer",
                "match": 78,
                "salary": "$100k - $145k",
                "demand": "High",
                "skills_match": ["✅ Docker", "✅ Linux", "✅ Python", "❌ K8s", "❌ Terraform"],
                "color": "#4CAF50"
            }
        ]
        
        for career in careers:
            with st.container():
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    st.markdown(f"""
                        <div style="background: {career['color']}; 
                                  padding: 1rem; border-radius: 10px; 
                                  text-align: center; color: white;">
                            <h2>{career['match']}%</h2>
                            <p>Match</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                        <div style="background: #f5f7fa; padding: 1rem; border-radius: 10px;">
                            <h3>{career['title']}</h3>
                            <p>💰 {career['salary']} • 📈 Demand: {career['demand']}</p>
                            <p>{' • '.join(career['skills_match'])}</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
    
    with tab4:
        st.subheader("📈 Your Learning Roadmap")
        
        # Timeline
        roadmap_data = pd.DataFrame({
            'Month': ['Month 1-2', 'Month 3-4', 'Month 5-6', 'Month 7-8'],
            'Focus': ['TypeScript & Advanced React', 
                     'GraphQL & State Management',
                     'Docker & Deployment',
                     'System Design & Interview Prep'],
            'Progress': [30, 0, 0, 0]
        })
        
        fig = go.Figure(data=[go.Table(
            header=dict(values=['Timeline', 'Focus Area', 'Progress'],
                       fill_color='#667eea',
                       font=dict(color='white', size=14),
                       align='left'),
            cells=dict(values=[roadmap_data.Month, 
                             roadmap_data.Focus,
                             [f"{p}% Complete" for p in roadmap_data.Progress]],
                      fill_color='#f5f7fa',
                      align='left'))
        ])
        
        fig.update_layout(height=300, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)
        
        # Recommended courses
        st.subheader("📚 Recommended Learning Resources")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
                <div class="skill-card">
                    <h4>TypeScript Masterclass</h4>
                    <p>Udemy • 20 hours</p>
                    <p>⭐⭐⭐⭐⭐ (4.8)</p>
                    <p style="color: #667eea;">Free • 67% off</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class="skill-card">
                    <h4>GraphQL with React</h4>
                    <p>Coursera • 15 hours</p>
                    <p>⭐⭐⭐⭐ (4.6)</p>
                    <p style="color: #667eea;">$49.99</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
                <div class="skill-card">
                    <h4>Docker & Kubernetes</h4>
                    <p>Pluralsight • 25 hours</p>
                    <p>⭐⭐⭐⭐⭐ (4.9)</p>
                    <p style="color: #667eea;">$29/month</p>
                </div>
            """, unsafe_allow_html=True)

else:
    # Welcome message when no analysis done
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.image("https://img.icons8.com/fluency/240/artificial-intelligence.png", width=200)
        st.markdown("""
            <div style="text-align: center; padding: 2rem;">
                <h2>Welcome to Your AI Career Copilot! 🚀</h2>
                <p style="font-size: 1.2rem; color: #666;">
                    Get started by entering your GitHub username or uploading your resume.
                    Our AI will analyze your skills and provide personalized career recommendations.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Features grid
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.markdown("""
                <div style="text-align: center; padding: 1rem;">
                    <h3>🔍 Analyze</h3>
                    <p>GitHub & Resume analysis</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col_b:
            st.markdown("""
                <div style="text-align: center; padding: 1rem;">
                    <h3>🎯 Match</h3>
                    <p>Career recommendations</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col_c:
            st.markdown("""
                <div style="text-align: center; padding: 1rem;">
                    <h3>📈 Grow</h3>
                    <p>Personalized learning paths</p>
                </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        <p>🚀 AI Developer Career Copilot • Built with Streamlit • © 2025</p>
        <p style="font-size: 0.9rem; opacity: 0.8;">Your personalized AI career guide</p>
    </div>
""", unsafe_allow_html=True)