import streamlit as st
from config import setup_page_config
from pages.instructor import render_instructor_mode
from pages.student import render_student_mode
from utils.storage import initialize_storage

def main():
    """Main application entry point"""
    setup_page_config()
    initialize_storage()
    
    # Header with mode toggle
    col1, col2, col3 = st.columns([2, 3, 2])
    
    with col1:
        st.title("📚 EduCanvas")
    
    with col3:
        mode = st.radio(
            "Mode",
            ["👨‍🏫 Instructor", "👨‍🎓 Student"],
            horizontal=True,
            key="mode_toggle"
        )
    
    st.divider()
    
    # Render appropriate mode
    if mode == "👨‍🏫 Instructor":
        render_instructor_mode()
    else:
        render_student_mode()

if __name__ == "__main__":
    main()
