import streamlit as st
from utils.storage import get_slides, get_quizzes, save_quiz_attempt, get_student_progress, update_student_progress
from utils.ui_components import render_slide_viewer, render_chat_interface, render_progress_indicator
from agents.learner_agent import LearnerAgent
from agents.tester_agent import TesterAgent
from agents.reviewer_agent import ReviewerAgent
from config import DEFAULT_COURSES, PASSING_THRESHOLD
import json

def render_student_mode():
    """Main render function for student mode"""
    
    st.sidebar.title("🎓 My Courses")
    
    # Student name
    if 'student_name' not in st.session_state:
        st.session_state.student_name = st.sidebar.text_input(
            "Enter Your Name",
            value="Student",
            key="student_name_input"
        )
    
    st.sidebar.divider()
    
    # Course selection
    if 'student_course' not in st.session_state:
        st.session_state.student_course = DEFAULT_COURSES[0]
    
    selected_course = st.sidebar.selectbox(
        "Select Course",
        DEFAULT_COURSES,
        key="student_course"
    )
    
    st.sidebar.divider()
    
    # Navigation
    page = st.sidebar.radio(
        "Navigation",
        ["📚 View Slides", "🤖 AI Study Companion", "✍️ Practice Quizzes", "📝 Take Quiz"]
    )
    
    # Render selected page
    if page == "📚 View Slides":
        render_view_slides(selected_course)
    elif page == "🤖 AI Study Companion":
        render_ai_companion(selected_course)
    elif page == "✍️ Practice Quizzes":
        render_practice_quizzes(selected_course)
    else:
        render_take_quiz(selected_course)

def render_view_slides(course_name: str):
    """Render slide viewing interface"""
    
    st.header(f"📚 Course Slides - {course_name}")
    
    slides = get_slides(course_name)
    
    if not slides:
        st.info("📭 No slides available yet. Your instructor will upload them soon!")
        return
    
    render_slide_viewer(slides)

def render_ai_companion(course_name: str):
    """Render AI study companion with learner agent"""
    
    st.header(f"🤖 AI Study Companion - {course_name}")
    
    slides = get_slides(course_name)
    
    if not slides:
        st.warning("⚠️ No slides available. Please wait for your instructor to upload slides.")
        return
    
    # Initialize learner agent
    if 'learner_agent' not in st.session_state:
        st.session_state.learner_agent = LearnerAgent()
    
    if 'learner_messages' not in st.session_state:
        st.session_state.learner_messages = []
    
    # Get student progress to identify weak areas
    student_name = st.session_state.get('student_name', 'Student')
    progress = get_student_progress(course_name, student_name)
    weak_areas = progress.get('weak_areas', [])
    
    # Show weak areas if any
    if weak_areas:
        st.info(f"🎯 **Focus Areas:** {', '.join(weak_areas)}")
        st.markdown("_Your AI tutor will pay special attention to these topics._")
    
    st.divider()
    
    # Select slides to study
    st.subheader("📖 Select Topic to Study")
    
    selected_slide_idx = st.selectbox(
        "Choose a slide/topic:",
        range(len(slides)),
        format_func=lambda x: f"Slide {x + 1}: {slides[x]['title']}"
    )
    
    selected_slide = slides[selected_slide_idx]
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"**Current Topic:** {selected_slide['title']}")
    
    with col2:
        if st.button("🔄 Start Fresh Session"):
            st.session_state.learner_agent.reset_conversation()
            st.session_state.learner_messages = []
            st.rerun()
    
    # Auto-teach mode
    if st.button("🎓 Explain This Topic", type="primary"):
        with st.spinner("🤖 Your AI tutor is preparing the explanation..."):
            slide_content = f"{selected_slide['title']}\n{selected_slide.get('content', '')}"
            
            response = st.session_state.learner_agent.teach_concept(
                slide_content=slide_content,
                weak_areas=weak_areas
            )
            
            st.session_state.learner_messages.append({
                'role': 'assistant',
                'content': response
            })
            st.rerun()
    
    # Display conversation
    st.divider()
    st.subheader("💬 Learning Session")
    
    # Show conversation history
    for msg in st.session_state.learner_messages:
        if msg['role'] == 'assistant':
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(msg['content'])
        else:
            with st.chat_message("user", avatar="👤"):
                st.markdown(msg['content'])
    
    # Chat input
    user_question = st.chat_input("Ask a question about this topic...")
    
    if user_question:
        # Add user message
        st.session_state.learner_messages.append({
            'role': 'user',
            'content': user_question
        })
        
        # Get AI response
        with st.spinner("🤖 Thinking..."):
            slide_content = f"{selected_slide['title']}\n{selected_slide.get('content', '')}"
            
            response = st.session_state.learner_agent.teach_concept(
                slide_content=slide_content,
                weak_areas=weak_areas,
                user_question=user_question
            )
            
            st.session_state.learner_messages.append({
                'role': 'assistant',
                'content': response
            })
            st.rerun()

def render_practice_quizzes(course_name: str):
    """Render practice quiz generation with tester agent"""
    
    st.header(f"✍️ Practice Quizzes - {course_name}")
    
    slides = get_slides(course_name)
    
    if not slides:
        st.warning("⚠️ No slides available for practice quizzes.")
        return
    
    # Initialize tester agent
    if 'tester_agent' not in st.session_state:
        st.session_state.tester_agent = TesterAgent()
    
    # Get student progress for focus areas
    student_name = st.session_state.get('student_name', 'Student')
    progress = get_student_progress(course_name, student_name)
    weak_areas = progress.get('weak_areas', [])
    
    st.subheader("🎯 Generate Practice Questions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_slide_idx = st.selectbox(
            "Select topic:",
            range(len(slides)),
            format_func=lambda x: f"Slide {x + 1}: {slides[x]['title']}"
        )
    
    with col2:
        difficulty = st.selectbox(
            "Difficulty Level",
            ["Easy", "Medium", "Hard"]
        )
    
    num_practice_questions = st.slider("Number of Questions", 1, 10, 3)
    
    if weak_areas:
        focus_on_weak = st.checkbox("Focus on my weak areas", value=True)
        if focus_on_weak:
            st.info(f"🎯 Will focus on: {', '.join(weak_areas)}")
    
    if st.button("🎲 Generate Practice Quiz", type="primary"):
        with st.spinner("🤖 Creating practice questions..."):
            selected_slide = slides[selected_slide_idx]
            slide_content = f"{selected_slide['title']}\n{selected_slide.get('content', '')}"
            
            focus_areas = weak_areas if weak_areas and focus_on_weak else None
            
            quiz_data = st.session_state.tester_agent.generate_practice_quiz(
                slide_content=slide_content,
                difficulty_level=difficulty,
                num_questions=num_practice_questions,
                focus_areas=focus_areas
            )
            
            if 'error' not in quiz_data:
                st.session_state.practice_quiz = quiz_data
                st.session_state.practice_answers = {}
                st.success("✅ Practice quiz generated!")
                st.rerun()
            else:
                st.error(f"Error: {quiz_data['error']}")
    
    # Display practice quiz
    if 'practice_quiz' in st.session_state:
        render_practice_quiz_interface(course_name)

def render_practice_quiz_interface(course_name: str):
    """Render practice quiz taking and review interface"""
    
    st.divider()
    st.subheader("📝 Practice Quiz")
    
    quiz = st.session_state.practice_quiz
    questions = quiz.get('questions', [])
    
    if 'practice_answers' not in st.session_state:
        st.session_state.practice_answers = {}
    
    # Display questions
    for idx, question in enumerate(questions):
        st.markdown(f"### Question {idx + 1}")
        st.markdown(question['question'])
        
        q_type = question.get('type', 'Short Answer')
        
        if q_type == 'MCQ' and 'options' in question:
            answer = st.radio(
                "Select your answer:",
                question['options'],
                key=f"practice_q_{idx}",
                index=None
            )
            if answer:
                st.session_state.practice_answers[idx] = answer
        else:
            answer = st.text_area(
                "Your answer:",
                key=f"practice_q_{idx}",
                height=100
            )
            if answer:
                st.session_state.practice_answers[idx] = answer
        
        st.divider()
    
    # Submit and review
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Submit & Review", type="primary"):
            if len(st.session_state.practice_answers) < len(questions):
                st.warning("Please answer all questions before submitting!")
            else:
                with st.spinner("🤖 Reviewing your answers..."):
                    # Use reviewer agent to analyze practice quiz
                    reviewer = ReviewerAgent()
                    
                    student_answers = [
                        {'answer': st.session_state.practice_answers.get(i, '')}
                        for i in range(len(questions))
                    ]
                    
                    analysis = reviewer.analyze_quiz_performance(
                        quiz_questions=questions,
                        student_answers=student_answers,
                        quiz_type="Practice"
                    )
                    
                    st.session_state.practice_analysis = analysis
                    
                    # Update student progress if needs remediation
                    if analysis.get('needs_remediation'):
                        student_name = st.session_state.get('student_name', 'Student')
                        current_progress = get_student_progress(course_name, student_name)
                        
                        # Update weak areas
                        new_weak_areas = analysis.get('weak_areas', [])
                        current_progress['weak_areas'] = list(set(
                            current_progress.get('weak_areas', []) + new_weak_areas
                        ))
                        
                        update_student_progress(course_name, student_name, current_progress)
                    
                    st.rerun()
    
    with col2:
        if st.button("🔄 New Practice Quiz"):
            if 'practice_quiz' in st.session_state:
                del st.session_state.practice_quiz
            if 'practice_answers' in st.session_state:
                del st.session_state.practice_answers
            if 'practice_analysis' in st.session_state:
                del st.session_state.practice_analysis
            st.rerun()
    
    # Show analysis if available
    if 'practice_analysis' in st.session_state:
        st.divider()
        st.subheader("📊 Your Performance")
        
        analysis = st.session_state.practice_analysis
        
        # Overall score
        render_progress_indicator(
            analysis.get('overall_score', 0),
            "Overall Score"
        )
        
        # Detailed feedback
        reviewer = ReviewerAgent()
        summary_report = reviewer.generate_summary_report(analysis)
        st.markdown(summary_report)

def render_take_quiz(course_name: str):
    """Render interface for taking official instructor quizzes"""
    
    st.header(f"📝 Take Quiz - {course_name}")
    
    quizzes = get_quizzes(course_name)
    
    if not quizzes:
        st.info("📭 No quizzes available yet. Check back later!")
        return
    
    # Select quiz
    quiz_titles = [f"{q['title']} - {q['type']}" for q in quizzes]
    selected_quiz_idx = st.selectbox(
        "Select Quiz",
        range(len(quizzes)),
        format_func=lambda x: quiz_titles[x]
    )
    
    selected_quiz = quizzes[selected_quiz_idx]
    
    st.markdown(f"**Quiz:** {selected_quiz['title']}")
    st.markdown(f"**Type:** {selected_quiz['type']}")
    st.markdown(f"**Questions:** {len(selected_quiz.get('questions', []))}")
    
    st.divider()
    
    # Take quiz
    if 'current_quiz_answers' not in st.session_state:
        st.session_state.current_quiz_answers = {}
    
    questions = selected_quiz.get('questions', [])
    
    for idx, question in enumerate(questions):
        st.markdown(f"### Question {idx + 1}")
        st.markdown(question['question'])
        
        if 'options' in question:
            answer = st.radio(
                "Select your answer:",
                question['options'],
                key=f"quiz_q_{idx}",
                index=None
            )
            if answer:
                st.session_state.current_quiz_answers[idx] = answer
        else:
            answer = st.text_area(
                "Your answer:",
                key=f"quiz_q_{idx}",
                height=150
            )
            if answer:
                st.session_state.current_quiz_answers[idx] = answer
        
        st.divider()
    
    # Submit quiz
    if st.button("📤 Submit Quiz", type="primary"):
        if len(st.session_state.current_quiz_answers) < len(questions):
            st.warning("⚠️ Please answer all questions before submitting!")
        else:
            with st.spinner("📊 Grading your quiz..."):
                # Prepare student answers
                student_answers = [
                    {'answer': st.session_state.current_quiz_answers.get(i, '')}
                    for i in range(len(questions))
                ]
                
                # Grade with reviewer agent
                reviewer = ReviewerAgent()
                analysis = reviewer.analyze_quiz_performance(
                    quiz_questions=questions,
                    student_answers=student_answers,
                    quiz_type=selected_quiz['type']
                )
                
                # Save attempt
                student_name = st.session_state.get('student_name', 'Student')
                save_quiz_attempt(
                    course_name=course_name,
                    quiz_id=selected_quiz['id'],
                    student_name=student_name,
                    attempt={
                        'answers': student_answers,
                        'analysis': analysis
                    }
                )
                
                # Update student progress
                if analysis.get('needs_remediation'):
                    current_progress = get_student_progress(course_name, student_name)
                    new_weak_areas = analysis.get('weak_areas', [])
                    current_progress['weak_areas'] = list(set(
                        current_progress.get('weak_areas', []) + new_weak_areas
                    ))
                    update_student_progress(course_name, student_name, current_progress)
                
                st.session_state.quiz_result = analysis
                st.success("✅ Quiz submitted successfully!")
                st.rerun()
    
    # Show results
    if 'quiz_result' in st.session_state:
        st.divider()
        st.subheader("📊 Quiz Results")
        
        analysis = st.session_state.quiz_result
        
        render_progress_indicator(
            analysis.get('overall_score', 0),
            "Final Score"
        )
        
        reviewer = ReviewerAgent()
        summary_report = reviewer.generate_summary_report(analysis)
        st.markdown(summary_report)
        
        if st.button("🔄 Take Another Quiz"):
            del st.session_state.current_quiz_answers
            del st.session_state.quiz_result
            st.rerun()
