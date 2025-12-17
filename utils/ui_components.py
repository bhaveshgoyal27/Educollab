import streamlit as st
from typing import List, Dict, Any

def render_slide_viewer(slides: List[Dict[str, Any]]):
    """Render slide viewer with navigation for slides and pages within PDFs"""
    if not slides:
        st.info("No slides uploaded yet.")
        return

    # Initialize session state for slide and page indices
    if 'current_slide_index' not in st.session_state:
        st.session_state.current_slide_index = 0

    if 'current_page_index' not in st.session_state:
        st.session_state.current_page_index = 0

    current_slide_idx = st.session_state.current_slide_index
    current_page_idx = st.session_state.current_page_index

    # Get current slide
    current_slide = slides[current_slide_idx]
    total_pages = current_slide.get('page_count', 1)

    # Reset page index if it exceeds the current slide's pages
    if current_page_idx >= total_pages:
        st.session_state.current_page_index = 0
        current_page_idx = 0

    # Slide navigation (between different files/slides)
    st.markdown("### 📁 Document Navigation")
    col1, col2, col3 = st.columns([1, 3, 1])

    with col1:
        if st.button("⬅️ Previous Document", disabled=(current_slide_idx == 0), key="prev_doc"):
            st.session_state.current_slide_index = max(0, current_slide_idx - 1)
            st.session_state.current_page_index = 0  # Reset to first page
            st.rerun()

    with col2:
        st.markdown(f"<h4 style='text-align: center;'>{current_slide['title']}</h4>",
                    unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: gray;'>Document {current_slide_idx + 1} of {len(slides)}</p>",
                    unsafe_allow_html=True)

    with col3:
        if st.button("Next Document ➡️", disabled=(current_slide_idx == len(slides) - 1), key="next_doc"):
            st.session_state.current_slide_index = min(len(slides) - 1, current_slide_idx + 1)
            st.session_state.current_page_index = 0  # Reset to first page
            st.rerun()

    st.divider()

    # Page navigation (within current PDF/slide if multi-page)
    if total_pages > 1:
        st.markdown("### 📄 Page Navigation")
        col1, col2, col3 = st.columns([1, 3, 1])

        with col1:
            if st.button("⬅️ Previous Page", disabled=(current_page_idx == 0), key="prev_page"):
                st.session_state.current_page_index = max(0, current_page_idx - 1)
                st.rerun()

        with col2:
            st.markdown(f"<h5 style='text-align: center;'>Page {current_page_idx + 1} of {total_pages}</h5>",
                        unsafe_allow_html=True)

        with col3:
            if st.button("Next Page ➡️", disabled=(current_page_idx == total_pages - 1), key="next_page"):
                st.session_state.current_page_index = min(total_pages - 1, current_page_idx + 1)
                st.rerun()

        # Optional: Page selector dropdown for quick navigation
        selected_page = st.selectbox(
            "Jump to page:",
            range(total_pages),
            index=current_page_idx,
            format_func=lambda x: f"Page {x + 1}",
            key="page_selector"
        )

        if selected_page != current_page_idx:
            st.session_state.current_page_index = selected_page
            st.rerun()

        st.divider()

    # Display current page
    if current_slide.get('pages'):
        try:
            # Get the current page image
            page_image = current_slide['pages'][current_page_idx]
            st.image(page_image, use_column_width=True)
        except Exception as e:
            st.error(f"Error displaying page: {str(e)}")
            st.info("The file may be corrupted or in an unsupported format.")
    else:
        st.info("Content not available for this slide.")

    # Display content/notes if available (show for first page or all pages)
    if current_slide.get('content') and current_page_idx == 0:
        with st.expander("📝 Document Content/Notes"):
            st.markdown(current_slide['content'][:1000] + "..." if len(current_slide.get('content', '')) > 1000 else current_slide.get('content', ''))

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