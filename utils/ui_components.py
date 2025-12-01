import streamlit as st
from typing import List, Dict, Any

def render_slide_viewer(slides: List[Dict[str, Any]]):
    """Render slide viewer with navigation"""
    if not slides:
        st.info("No slides uploaded yet.")
        return
    
    if 'current_slide_index' not in st.session_state:
        st.session_state.current_slide_index = 0
    
    current_index = st.session_state.current_slide_index
    
    # Navigation controls
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        if st.button("⬅️ Previous", disabled=(current_index == 0)):
            st.session_state.current_slide_index = max(0, current_index - 1)
            st.rerun()
    
    with col2:
        st.markdown(f"<h4 style='text-align: center;'>Slide {current_index + 1} of {len(slides)}</h4>", 
                   unsafe_allow_html=True)
    
    with col3:
        if st.button("Next ➡️", disabled=(current_index == len(slides) - 1)):
            st.session_state.current_slide_index = min(len(slides) - 1, current_index + 1)
            st.rerun()
    
    # Display current slide
    st.divider()
    current_slide = slides[current_index]
    
    st.markdown(f"### {current_slide['title']}")
    
    if current_slide.get('file'):
        st.image(current_slide['file'], use_column_width=True)
    
    if current_slide.get('content'):
        st.markdown(current_slide['content'])

def render_quiz_card(quiz: Dict[str, Any], show_actions: bool = False):
    """Render a quiz card"""
    st.markdown(f"""
        <div class="quiz-card">
            <h3>{quiz['title']}</h3>
            <p><strong>Type:</strong> {quiz['type']}</p>
            <p><strong>Questions:</strong> {len(quiz.get('questions', []))}</p>
            <p><strong>Created:</strong> {quiz.get('created_at', 'N/A')}</p>
        </div>
    """, unsafe_allow_html=True)
    
    if show_actions:
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"View Details - {quiz['id']}", key=f"view_{quiz['id']}"):
                return 'view'
        with col2:
            if st.button(f"View Reports - {quiz['id']}", key=f"report_{quiz['id']}"):
                return 'report'
    return None

def render_progress_indicator(score: float, label: str = "Score"):
    """Render a progress indicator with score"""
    color = "#4CAF50" if score >= 70 else "#FFC107" if score >= 50 else "#F44336"
    
    st.markdown(f"""
        <div style="background-color: #f0f0f0; border-radius: 10px; padding: 10px; margin: 10px 0;">
            <p style="margin: 0; font-weight: bold;">{label}</p>
            <div style="background-color: #ddd; border-radius: 5px; height: 20px; margin-top: 5px;">
                <div style="background-color: {color}; width: {score}%; height: 100%; border-radius: 5px;
                            display: flex; align-items: center; justify-content: center;">
                    <span style="color: white; font-weight: bold; font-size: 12px;">{score:.1f}%</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_chat_interface(messages: List[Dict[str, str]], key_prefix: str = "chat"):
    """Render a chat-like interface for agent conversations"""
    for idx, message in enumerate(messages):
        role = message['role']
        content = message['content']
        
        if role == 'user':
            st.markdown(f"""
                <div style="background-color: #E3F2FD; padding: 10px; border-radius: 10px; 
                            margin: 5px 0; text-align: right;">
                    <strong>You:</strong> {content}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="background-color: #F5F5F5; padding: 10px; border-radius: 10px; margin: 5px 0;">
                    <strong>AI Assistant:</strong> {content}
                </div>
            """, unsafe_allow_html=True)
