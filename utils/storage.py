import streamlit as st
from datetime import datetime
import json
from typing import List, Dict, Any

def initialize_storage():
    """Initialize session state storage"""
    if 'courses' not in st.session_state:
        st.session_state.courses = {}
    
    if 'current_course' not in st.session_state:
        st.session_state.current_course = None
    
    if 'slides' not in st.session_state:
        st.session_state.slides = {}
    
    if 'quizzes' not in st.session_state:
        st.session_state.quizzes = {}
    
    if 'quiz_attempts' not in st.session_state:
        st.session_state.quiz_attempts = {}
    
    if 'student_progress' not in st.session_state:
        st.session_state.student_progress = {}

def save_slides(course_name: str, slides: List[Dict[str, Any]]):
    """Save slides for a course"""
    if course_name not in st.session_state.slides:
        st.session_state.slides[course_name] = []
    
    st.session_state.slides[course_name].extend(slides)

def get_slides(course_name: str) -> List[Dict[str, Any]]:
    """Get slides for a course"""
    return st.session_state.slides.get(course_name, [])

def save_quiz(course_name: str, quiz: Dict[str, Any]):
    """Save a quiz for a course"""
    if course_name not in st.session_state.quizzes:
        st.session_state.quizzes[course_name] = []
    
    quiz['id'] = f"quiz_{len(st.session_state.quizzes[course_name])}"
    quiz['created_at'] = datetime.now().isoformat()
    st.session_state.quizzes[course_name].append(quiz)
    return quiz['id']

def get_quizzes(course_name: str) -> List[Dict[str, Any]]:
    """Get all quizzes for a course"""
    return st.session_state.quizzes.get(course_name, [])

def save_quiz_attempt(course_name: str, quiz_id: str, student_name: str, attempt: Dict[str, Any]):
    """Save a student's quiz attempt"""
    key = f"{course_name}_{quiz_id}"
    if key not in st.session_state.quiz_attempts:
        st.session_state.quiz_attempts[key] = {}
    
    if student_name not in st.session_state.quiz_attempts[key]:
        st.session_state.quiz_attempts[key][student_name] = []
    
    attempt['timestamp'] = datetime.now().isoformat()
    st.session_state.quiz_attempts[key][student_name].append(attempt)

def get_quiz_attempts(course_name: str, quiz_id: str) -> Dict[str, List[Dict[str, Any]]]:
    """Get all attempts for a quiz"""
    key = f"{course_name}_{quiz_id}"
    return st.session_state.quiz_attempts.get(key, {})

def update_student_progress(course_name: str, student_name: str, progress: Dict[str, Any]):
    """Update student's learning progress"""
    key = f"{course_name}_{student_name}"
    st.session_state.student_progress[key] = progress

def get_student_progress(course_name: str, student_name: str) -> Dict[str, Any]:
    """Get student's learning progress"""
    key = f"{course_name}_{student_name}"
    return st.session_state.student_progress.get(key, {
        'weak_areas': [],
        'quiz_history': [],
        'learning_context': ''
    })
