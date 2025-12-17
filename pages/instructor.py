import streamlit as st
from utils.storage import save_slides, get_slides, save_quiz, get_quizzes, get_quiz_attempts
from utils.ui_components import render_quiz_card, render_progress_indicator
from utils.pdf_handler import pdf_to_images, is_pdf, is_image, extract_text_from_pdf, get_pdf_page_count
from agents.quiz_generator import QuizGeneratorAgent
from agents.reviewer_agent import ReviewerAgent
from config import DEFAULT_COURSES, QUIZ_TYPES
import json

def render_instructor_mode():
    """Main render function for instructor mode"""

    st.sidebar.title("📚 Course Management")

    # Course selection
    if 'instructor_course' not in st.session_state:
        st.session_state.instructor_course = DEFAULT_COURSES[0]

    selected_course = st.sidebar.selectbox(
        "Select Course",
        DEFAULT_COURSES,
        key="instructor_course"
    )

    st.sidebar.divider()

    # Navigation
    page = st.sidebar.radio(
        "Navigation",
        ["📄 Manage Slides", "✍️ Create Quiz", "📊 Quiz Reports"]
    )

    # Render selected page
    if page == "📄 Manage Slides":
        render_slides_management(selected_course)
    elif page == "✍️ Create Quiz":
        render_quiz_creation(selected_course)
    else:
        render_quiz_reports(selected_course)

def render_slides_management(course_name: str):
    """Render slide upload and management interface"""

    st.header(f"📄 Manage Slides - {course_name}")

    # Upload slides
    st.subheader("Upload New Slides")

    col1, col2 = st.columns([3, 1])

    with col1:
        uploaded_files = st.file_uploader(
            "Upload slides (PDF, Images)",
            type=['pdf', 'png', 'jpg', 'jpeg'],
            accept_multiple_files=True,
            key=f"slide_upload_{course_name}"
        )

    with col2:
        if st.button("📤 Upload Slides", type="primary"):
            if uploaded_files:
                slides = []
                current_slide_count = len(get_slides(course_name))

                with st.spinner("Processing files..."):
                    for file in uploaded_files:
                        file_bytes = file.getvalue()
                        file_type = file.type if hasattr(file, 'type') else 'unknown'

                        # Check if PDF
                        if is_pdf(file_bytes) or file_type == 'application/pdf':
                            # Convert PDF to images and extract text
                            try:
                                images = pdf_to_images(file_bytes)
                                text_content = extract_text_from_pdf(file_bytes)

                                if images:
                                    # Store PDF as single slide with multiple pages
                                    slides.append({
                                        'id': f"slide_{current_slide_count + len(slides)}",
                                        'title': file.name,
                                        'file_type': 'pdf',
                                        'pages': images,  # List of image bytes for each page
                                        'page_count': len(images),
                                        'order': current_slide_count + len(slides),
                                        'content': text_content,
                                        'original_filename': file.name
                                    })
                                else:
                                    st.warning(f"⚠️ Could not process PDF: {file.name}")
                            except Exception as e:
                                st.error(f"❌ Error processing {file.name}: {str(e)}")

                        # Check if image
                        elif is_image(file_bytes):
                            slides.append({
                                'id': f"slide_{current_slide_count + len(slides)}",
                                'title': file.name,
                                'file_type': 'image',
                                'pages': [file_bytes],  # Single page for images
                                'page_count': 1,
                                'order': current_slide_count + len(slides),
                                'content': f"Image: {file.name}",
                                'original_filename': file.name
                            })
                        else:
                            st.warning(f"⚠️ Unsupported file type: {file.name}")

                if slides:
                    save_slides(course_name, slides)
                    st.success(f"✅ Uploaded {len(slides)} slide(s)!")
                    st.rerun()
                else:
                    st.error("❌ No valid slides to upload!")

    st.divider()

    # Display existing slides
    st.subheader("Uploaded Slides")

    existing_slides = get_slides(course_name)

    if existing_slides:
        st.info(f"📚 Total slide sets: {len(existing_slides)}")

        for idx, slide in enumerate(existing_slides):
            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                page_info = f" ({slide['page_count']} pages)" if slide.get('page_count', 1) > 1 else ""
                st.markdown(f"**{idx + 1}.** {slide['title']}{page_info}")

            with col2:
                with st.expander("Preview"):
                    if slide.get('pages'):
                        try:
                            # Show first page as preview
                            st.image(slide['pages'][0], use_column_width=True)
                            if slide.get('page_count', 1) > 1:
                                st.caption(f"Showing page 1 of {slide['page_count']}")
                        except Exception as e:
                            st.error(f"Error displaying preview: {str(e)}")
                    else:
                        st.info("Preview not available")

            with col3:
                if st.button(f"🗑️ Remove", key=f"remove_{slide['id']}"):
                    existing_slides.pop(idx)
                    st.session_state.slides[course_name] = existing_slides
                    st.rerun()
    else:
        st.info("No slides uploaded yet. Upload slides to get started!")

def render_quiz_creation(course_name: str):
    """Render quiz creation interface"""

    st.header(f"✍️ Create Quiz - {course_name}")

    # Quiz creation tabs
    tab1, tab2 = st.tabs(["🖊️ Manual Quiz", "🤖 AI-Assisted Quiz"])

    with tab1:
        render_manual_quiz_creation(course_name)

    with tab2:
        render_ai_quiz_creation(course_name)

def render_manual_quiz_creation(course_name: str):
    """Render manual quiz creation placeholder"""

    st.subheader("Manual Quiz Creation")

    st.info("🚧 Manual quiz creation interface - Coming Soon!")

    st.markdown("""
    **Features (To Be Implemented):**
    - Add questions manually
    - Choose question types (MCQ, Short Answer, Essay)
    - Set point values
    - Add answer keys
    - Preview quiz before publishing
    """)

    if st.button("Create Manual Quiz (Placeholder)", type="primary"):
        st.success("Manual quiz creation feature will be implemented here!")

def render_ai_quiz_creation(course_name: str):
    """Render AI-assisted quiz creation"""

    st.subheader("AI-Assisted Quiz Generation")

    slides = get_slides(course_name)

    if not slides:
        st.warning("⚠️ Please upload slides first before creating AI-generated quizzes.")
        return

    # Quiz configuration
    col1, col2 = st.columns(2)

    with col1:
        quiz_title = st.text_input("Quiz Title", value="Quiz 1")
        quiz_type = st.selectbox("Quiz Type", QUIZ_TYPES)

    with col2:
        num_questions = st.number_input("Number of Questions", min_value=1, max_value=20, value=5)

    # Select slides to include
    st.subheader("Select Slides for Quiz")

    slide_options = [
        f"{idx + 1}. {slide['title']}" + (f" ({slide['page_count']} pages)" if slide.get('page_count', 1) > 1 else "")
        for idx, slide in enumerate(slides)
    ]

    selected_slide_indices = st.multiselect(
        "Choose slides/documents to base the quiz on:",
        range(len(slides)),
        format_func=lambda x: slide_options[x],
        default=list(range(min(3, len(slides))))
    )

    # Learning objectives
    learning_objectives = st.text_area(
        "Learning Objectives",
        placeholder="Enter the learning objectives for this quiz...\nExample:\n- Understand basic concepts of data structures\n- Apply algorithms to solve problems\n- Analyze time complexity",
        height=150
    )

    st.divider()

    # Generate quiz
    if st.button("🚀 Generate Quiz", type="primary"):
        if not selected_slide_indices:
            st.error("Please select at least one slide!")
        elif not learning_objectives:
            st.error("Please enter learning objectives!")
        else:
            with st.spinner("🤖 AI is generating quiz questions..."):
                # Compile slide content
                slide_content = "\n\n".join([
                    f"Slide {i+1}: {slides[i]['title']}\n{slides[i]['content']}"
                    for i in selected_slide_indices
                ])

                # Generate quiz
                agent = QuizGeneratorAgent()
                quiz_data = agent.generate_quiz(
                    slide_content=slide_content,
                    learning_objectives=learning_objectives,
                    quiz_type=quiz_type,
                    num_questions=num_questions
                )

                if 'error' in quiz_data:
                    st.error(f"Error generating quiz: {quiz_data['error']}")
                else:
                    st.session_state.generated_quiz = {
                        'title': quiz_title,
                        'type': quiz_type,
                        'learning_objectives': learning_objectives,
                        'questions': quiz_data.get('questions', [])
                    }
                    st.success("✅ Quiz generated! Review below:")

    # Review and modify generated quiz
    if 'generated_quiz' in st.session_state:
        render_quiz_review(course_name)

def render_quiz_review(course_name: str):
    """Render quiz review and modification interface"""

    st.divider()
    st.subheader("📝 Review Generated Quiz")

    quiz = st.session_state.generated_quiz

    st.markdown(f"**Title:** {quiz['title']}")
    st.markdown(f"**Type:** {quiz['type']}")
    st.markdown(f"**Questions:** {len(quiz['questions'])}")

    st.divider()

    # Display each question for review
    for idx, question in enumerate(quiz['questions']):
        with st.expander(f"Question {idx + 1}: {question.get('question', '')[:100]}...", expanded=False):
            st.markdown(f"**Question:** {question['question']}")

            if 'options' in question:
                st.markdown("**Options:**")
                for opt in question['options']:
                    st.markdown(f"  {opt}")
                st.markdown(f"**Correct Answer:** {question.get('correct_answer', 'N/A')}")

            st.markdown(f"**Learning Objective:** {question.get('learning_objective', 'N/A')}")
            st.markdown(f"**Cognitive Level:** {question.get('cognitive_level', 'N/A')}")

            if 'explanation' in question:
                st.markdown(f"**Explanation:** {question['explanation']}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"✏️ Modify", key=f"modify_{idx}"):
                    st.info("Modification interface - To be implemented")
            with col2:
                if st.button(f"🗑️ Remove", key=f"remove_q_{idx}"):
                    quiz['questions'].pop(idx)
                    st.rerun()

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("✅ Approve & Publish Quiz", type="primary"):
            quiz_id = save_quiz(course_name, quiz)
            st.success(f"🎉 Quiz published successfully! Quiz ID: {quiz_id}")
            del st.session_state.generated_quiz
            st.rerun()

    with col2:
        if st.button("🔄 Regenerate"):
            del st.session_state.generated_quiz
            st.rerun()

    with col3:
        if st.button("❌ Cancel"):
            del st.session_state.generated_quiz
            st.rerun()

def render_quiz_reports(course_name: str):
    """Render quiz reports and analytics"""

    st.header(f"📊 Quiz Reports - {course_name}")

    quizzes = get_quizzes(course_name)

    if not quizzes:
        st.info("No quizzes created yet. Create a quiz to see reports!")
        return

    # Select quiz
    quiz_titles = [f"{q['title']} ({q['id']})" for q in quizzes]
    selected_quiz_idx = st.selectbox(
        "Select Quiz",
        range(len(quizzes)),
        format_func=lambda x: quiz_titles[x]
    )

    selected_quiz = quizzes[selected_quiz_idx]

    st.divider()

    # Get quiz attempts
    attempts = get_quiz_attempts(course_name, selected_quiz['id'])

    if not attempts:
        st.info("No student submissions yet for this quiz.")
        return

    # Display summary statistics
    st.subheader("📈 Summary Statistics")

    total_students = len(attempts)
    st.metric("Total Submissions", total_students)

    # Student results table
    st.subheader("🎓 Student Results")

    for student_name, student_attempts in attempts.items():
        with st.expander(f"👤 {student_name} - {len(student_attempts)} attempt(s)"):
            for idx, attempt in enumerate(student_attempts):
                st.markdown(f"**Attempt {idx + 1}** - {attempt.get('timestamp', 'N/A')}")

                if 'analysis' in attempt:
                    analysis = attempt['analysis']

                    # Show score
                    render_progress_indicator(
                        analysis.get('overall_score', 0),
                        "Overall Score"
                    )

                    # Show feedback
                    st.markdown("**📝 Detailed Feedback:**")

                    # Individual question feedback
                    for q_idx, q_score in enumerate(analysis.get('question_scores', [])):
                        st.markdown(f"""
                        **Question {q_score['question_number']}:** 
                        {q_score['points_earned']}/{q_score['max_points']} points
                        
                        {q_score.get('feedback', '')}
                        """)

                    # Weak areas
                    if analysis.get('weak_areas'):
                        st.markdown("**⚠️ Areas for Improvement:**")
                        for area in analysis['weak_areas']:
                            st.markdown(f"  • {area}")

                    # Strong areas
                    if analysis.get('strong_areas'):
                        st.markdown("**✅ Strengths:**")
                        for area in analysis['strong_areas']:
                            st.markdown(f"  • {area}")

                    # Recommendations
                    if analysis.get('recommendations'):
                        st.markdown("**💡 Recommendations:**")
                        for rec in analysis['recommendations']:
                            st.markdown(f"  • {rec}")

                st.divider()