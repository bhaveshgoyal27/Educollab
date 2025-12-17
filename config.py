import streamlit as st
import os

# API Configuration - Add your API keys here
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-6aAUuLKU6N1Nfm9jfX-hvg")


os.environ['API_KEY'] = "sk-6aAUuLKU6N1Nfm9jfX-hvg"
os.environ['OPENAI_API_KEY'] = "sk-6aAUuLKU6N1Nfm9jfX-hvg"
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
    """Configure Streamlit page settings with complete Canvas theme"""
    st.set_page_config(
        page_title="EduCanvas - Learning Management System",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Complete Canvas LMS styling matching the screenshots
    st.markdown("""
        <style>
        /* Import Canvas-like fonts */
        @import url('https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700&display=swap');
        
        /* Cornell/Canvas Color Palette */
        :root {
            --cornell-red: #B31B1B;
            --cornell-dark: #8B1616;
            --canvas-dark-bg: #2D3B45;
            --canvas-light-bg: #F5F5F5;
            --canvas-white: #FFFFFF;
            --canvas-border: #C7CDD1;
            --canvas-text: #2D2D2D;
            --canvas-link: #B31B1B;
            --canvas-hover: #F0F0F0;
            --module-bg: #F9F9F9;
            --module-border: #DFDFDF;
        }
        
        /* Global font */
        * {
            font-family: 'Lato', 'Helvetica Neue', Helvetica, Arial, sans-serif;
        }
        
        /* Main container - Canvas light gray */
        .main {
            background-color: var(--canvas-light-bg);
            padding: 0;
        }
        
        /* Remove default Streamlit padding */
        .block-container {
            padding: 1rem 3rem 2rem 3rem;
            max-width: 100%;
        }
        
        /* Sidebar - Cornell dark theme */
        section[data-testid="stSidebar"] {
            background-color: var(--cornell-dark);
            border-right: 1px solid #1A2329;
        }
        
        section[data-testid="stSidebar"] * {
            color: white !important;
        }
        
        /* Sidebar links */
        section[data-testid="stSidebar"] .stRadio > div > label {
            background-color: transparent;
            padding: 12px 20px;
            margin: 2px 0;
            border-radius: 0;
            transition: background-color 0.15s ease;
            font-size: 0.95rem;
        }
        
        section[data-testid="stSidebar"] .stRadio > div > label:hover {
            background-color: rgba(255, 255, 255, 0.1);
        }
        
        section[data-testid="stSidebar"] .stRadio > div > label[data-checked="true"] {
            background-color: rgba(255, 255, 255, 0.15);
            font-weight: 600;
        }
        
        /* Breadcrumb navigation (like Canvas) */
        .breadcrumb {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 1rem 0;
            font-size: 0.9rem;
            color: #666;
        }
        
        .breadcrumb a {
            color: var(--cornell-red);
            text-decoration: none;
        }
        
        .breadcrumb a:hover {
            text-decoration: underline;
        }
        
        .breadcrumb-separator {
            color: #999;
            margin: 0 0.5rem;
        }
        
        /* Page title */
        h1 {
            color: var(--canvas-text);
            font-weight: 400;
            font-size: 1.75rem;
            margin: 1rem 0;
            padding: 0;
            border: none;
        }
        
        /* Section headers */
        h2 {
            color: var(--canvas-text);
            font-weight: 600;
            font-size: 1.25rem;
            margin: 1.5rem 0 1rem 0;
        }
        
        /* Canvas Module Sections */
        div[data-testid="stExpander"] {
            background-color: white;
            border: 1px solid var(--module-border);
            border-radius: 0;
            margin-bottom: 0 !important;
            box-shadow: none;
            border-top: none;
        }
        
        div[data-testid="stExpander"]:first-of-type {
            border-top: 1px solid var(--module-border);
            border-radius: 4px 4px 0 0;
        }
        
        div[data-testid="stExpander"]:last-of-type {
            border-radius: 0 0 4px 4px;
        }
        
        /* Module header (collapsed state) */
        div[data-testid="stExpander"] > summary {
            background-color: var(--module-bg);
            color: var(--canvas-text) !important;
            padding: 1rem 1.25rem;
            font-weight: 600;
            font-size: 1rem;
            border: none;
            border-left: 3px solid transparent;
            transition: all 0.15s ease;
        }
        
        div[data-testid="stExpander"] > summary:hover {
            background-color: var(--canvas-hover);
            border-left-color: var(--cornell-red);
        }
        
        /* Expanded module */
        div[data-testid="stExpander"][open] > summary {
            background-color: white;
            border-left-color: var(--cornell-red);
            border-bottom: 1px solid var(--module-border);
        }
        
        /* Module content area */
        div[data-testid="stExpander"] > div {
            padding: 0;
            background-color: white;
        }
        
        /* Module items (slides, readings, etc) */
        .module-item {
            padding: 1rem 1.5rem;
            border-bottom: 1px solid var(--module-border);
            display: flex;
            align-items: center;
            gap: 1rem;
            transition: background-color 0.15s ease;
        }
        
        .module-item:hover {
            background-color: var(--module-bg);
        }
        
        .module-item:last-child {
            border-bottom: none;
        }
        
        .module-item-icon {
            color: #666;
            font-size: 1.1rem;
            width: 24px;
            text-align: center;
        }
        
        .module-item-title {
            flex: 1;
            color: var(--cornell-red);
            font-weight: 500;
            text-decoration: none;
        }
        
        .module-item-title:hover {
            text-decoration: underline;
        }
        
        /* Buttons - Canvas style */
        .stButton > button {
            background-color: var(--cornell-red);
            color: white;
            border: 1px solid var(--cornell-red);
            border-radius: 4px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            font-size: 0.9rem;
            transition: all 0.15s ease;
        }
        
        .stButton > button:hover {
            background-color: var(--cornell-dark);
            border-color: var(--cornell-dark);
        }
        
        /* Secondary button */
        .stButton > button[kind="secondary"] {
            background-color: white;
            color: var(--cornell-red);
            border: 1px solid var(--cornell-red);
        }
        
        .stButton > button[kind="secondary"]:hover {
            background-color: var(--module-bg);
        }
        
        /* Links - Cornell red */
        a {
            color: var(--cornell-red);
            text-decoration: none;
            font-weight: 500;
        }
        
        a:hover {
            text-decoration: underline;
        }
        
        /* Input fields */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div,
        .stMultiSelect > div > div {
            border: 1px solid var(--canvas-border);
            border-radius: 4px;
            padding: 0.5rem;
            font-size: 0.9rem;
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: var(--cornell-red);
            outline: none;
            box-shadow: 0 0 0 2px rgba(179, 27, 27, 0.1);
        }
        
        /* File upload - Canvas style */
        div[data-testid="stFileUploadDropzone"] {
            border: 2px dashed var(--canvas-border);
            border-radius: 4px;
            background-color: white;
            padding: 2rem;
        }
        
        div[data-testid="stFileUploadDropzone"]:hover {
            border-color: var(--cornell-red);
            background-color: var(--module-bg);
        }
        
        /* Tabs - Canvas style */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0;
            background-color: white;
            border-bottom: 1px solid var(--canvas-border);
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: transparent;
            border: none;
            border-bottom: 3px solid transparent;
            color: var(--canvas-text);
            padding: 0.75rem 1.25rem;
            font-weight: 500;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            color: var(--cornell-red);
        }
        
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            border-bottom-color: var(--cornell-red);
            color: var(--cornell-red);
            font-weight: 600;
        }
        
        /* Alert boxes */
        .stAlert {
            border-radius: 4px;
            border-left: 4px solid;
            padding: 1rem;
            margin: 1rem 0;
        }
        
        div[data-baseweb="notification"][kind="info"] {
            background-color: #E8F4FD;
            border-left-color: #0770A3;
        }
        
        div[data-baseweb="notification"][kind="success"] {
            background-color: #E5F7E6;
            border-left-color: #00AC18;
        }
        
        div[data-baseweb="notification"][kind="warning"] {
            background-color: #FFF4E5;
            border-left-color: #FC5E13;
        }
        
        div[data-baseweb="notification"][kind="error"] {
            background-color: #FEE;
            border-left-color: var(--cornell-red);
        }
        
        /* Metrics/Stats - Dashboard style */
        div[data-testid="stMetric"] {
            background: white;
            border: 1px solid var(--canvas-border);
            border-radius: 4px;
            padding: 1.25rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        }
        
        div[data-testid="stMetric"] label {
            color: #666;
            font-weight: 600;
            font-size: 0.85rem;
            text-transform: uppercase;
        }
        
        div[data-testid="stMetric"] [data-testid="stMetricValue"] {
            color: var(--cornell-red);
            font-size: 2rem;
            font-weight: 700;
        }
        
        /* Progress bar */
        .stProgress > div > div > div {
            background-color: var(--cornell-red);
        }
        
        .stProgress > div > div {
            background-color: var(--module-bg);
        }
        
        /* Data tables */
        .stDataFrame {
            border: 1px solid var(--canvas-border);
            border-radius: 4px;
        }
        
        /* Divider */
        hr {
            border: none;
            border-top: 1px solid var(--canvas-border);
            margin: 2rem 0;
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 12px;
            height: 12px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--module-bg);
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--canvas-border);
            border-radius: 6px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #999;
        }
        
        /* PDF Viewer styling (Canvas embedded PDF look) */
        iframe[title*="pdf"] {
            border: 1px solid var(--canvas-border);
            border-radius: 4px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        }
        
        /* Download button for PDFs */
        .stDownloadButton > button {
            background-color: white;
            color: var(--cornell-red);
            border: 1px solid var(--cornell-red);
        }
        
        .stDownloadButton > button:hover {
            background-color: var(--module-bg);
        }
        
        /* Collapse All button */
        .collapse-button {
            background-color: white;
            color: #666;
            border: 1px solid var(--canvas-border);
            padding: 0.5rem 1rem;
            border-radius: 4px;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.15s ease;
        }
        
        .collapse-button:hover {
            background-color: var(--module-bg);
            border-color: #999;
        }
        
        /* Course info header */
        .course-header {
            background-color: white;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border: 1px solid var(--canvas-border);
            border-radius: 4px;
        }
        
        .course-title {
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--canvas-text);
            margin-bottom: 0.5rem;
        }
        
        .course-meta {
            color: #666;
            font-size: 0.9rem;
        }
        
        /* Navigation buttons (Previous/Next) */
        .nav-button {
            display: inline-block;
            padding: 0.75rem 1.25rem;
            background-color: white;
            color: var(--cornell-red);
            border: 1px solid var(--canvas-border);
            border-radius: 4px;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.15s ease;
        }
        
        .nav-button:hover {
            background-color: var(--module-bg);
            border-color: var(--cornell-red);
        }
        
        /* Canvas module list container */
        .module-list {
            background-color: white;
            border: 1px solid var(--canvas-border);
            border-radius: 4px;
            margin: 1rem 0;
        }
        
        /* Canvas page controls bar */
        .page-controls {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem;
            background-color: white;
            border: 1px solid var(--canvas-border);
            border-radius: 4px;
            margin-bottom: 1rem;
        }
        
        /* Remove Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

def get_openai_client():
    """Get OpenAI client with API key"""
    API_KEY = "sk-6aAUuLKU6N1Nfm9jfX-hvg"
    OPENAI_API_KEY = "sk-6aAUuLKU6N1Nfm9jfX-hvg"
    BASE_URL = "https://api.ai.it.cornell.edu/"
    OPENAI_BASE_URL = "https://api.ai.it.cornell.edu/"
    from openai import OpenAI
    return OpenAI()
