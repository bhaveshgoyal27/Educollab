import streamlit as st
import os

# API Configuration - Add your API keys here
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY_HERE")

# Model Configuration
DEFAULT_MODEL = "gpt-4o"
AGENT_MODEL = "gpt-4o"

# Quiz Configuration
QUIZ_TYPES = ["Multiple Choice (MCQ)", "Conversational", "Long Answer"]
PASSING_THRESHOLD = 90  # Percentage threshold for reviewer agent feedback

# Course Configuration
DEFAULT_COURSES = [
    "Introduction to Computer Science",
    "Data Structures and Algorithms",
    "Machine Learning Fundamentals",
    "Web Development"
]

def setup_page_config():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="EduCanvas - AI-Powered Learning Platform",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for Canvas-like UI
    st.markdown("""
        <style>
        .main {
            background-color: #f5f5f5;
        }
        .stButton>button {
            border-radius: 8px;
            border: 1px solid #ddd;
            padding: 0.5rem 1rem;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px 8px 0 0;
            padding: 0.5rem 1.5rem;
        }
        .quiz-card {
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)

def get_openai_client():
    """Get OpenAI client with API key"""
    from openai import OpenAI
    return OpenAI(api_key=OPENAI_API_KEY)
