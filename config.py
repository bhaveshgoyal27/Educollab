import streamlit as st
import os

# API Configuration - Add your API keys here
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-6aAUuLKU6N1Nfm9jfX-hvg")


os.environ['API_KEY'] = "sk-nsjrhU0f3oKGYC9VWee1_g"
os.environ['OPENAI_API_KEY'] = "sk-nsjrhU0f3oKGYC9VWee1_g"
os.environ['TAVILY_API_KEY'] = "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"
os.environ['BASE_URL'] = "https://api.ai.it.cornell.edu/"
os.environ['OPENAI_BASE_URL'] = "https://api.ai.it.cornell.edu/"

from dotenv import load_dotenv

load_dotenv()  # Loads variables from a local .env if present


# Model Configuration
DEFAULT_MODEL = "openai.gpt-4o"
AGENT_MODEL = "openai.gpt-4o"

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
    API_KEY = "sk-nsjrhU0f3oKGYC9VWee1_g"
    OPENAI_API_KEY = "sk-nsjrhU0f3oKGYC9VWee1_g"
    BASE_URL = "https://api.ai.it.cornell.edu/"
    OPENAI_BASE_URL = "https://api.ai.it.cornell.edu/"
    from openai import OpenAI
    return OpenAI()
