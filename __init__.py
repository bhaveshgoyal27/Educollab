# utils/__init__.py
"""Utility functions and components for EduCanvas"""

from .storage import (
    initialize_storage,
    save_slides,
    get_slides,
    save_quiz,
    get_quizzes,
    save_quiz_attempt,
    get_quiz_attempts,
    update_student_progress,
    get_student_progress
)

from .ui_components import (
    render_slide_viewer,
    render_quiz_card,
    render_progress_indicator,
    render_chat_interface
)

from .pdf_handler import (
    pdf_to_images,
    is_pdf,
    is_image,
    extract_text_from_pdf,
    get_pdf_page_count,
    pdf_to_base64
)

__all__ = [
    'initialize_storage',
    'save_slides',
    'get_slides',
    'save_quiz',
    'get_quizzes',
    'save_quiz_attempt',
    'get_quiz_attempts',
    'update_student_progress',
    'get_student_progress',
    'render_slide_viewer',
    'render_quiz_card',
    'render_progress_indicator',
    'render_chat_interface',
    'pdf_to_images',
    'is_pdf',
    'is_image',
    'extract_text_from_pdf',
    'get_pdf_page_count',
    'pdf_to_base64'
]


# agents/__init__.py
"""AI Agents for EduCanvas platform"""

from .quiz_generator import QuizGeneratorAgent
from .learner_agent import LearnerAgent
from .tester_agent import TesterAgent
from .reviewer_agent import ReviewerAgent

__all__ = [
    'QuizGeneratorAgent',
    'LearnerAgent',
    'TesterAgent',
    'ReviewerAgent'
]


# pages/__init__.py
"""Page modules for EduCanvas application"""

from .instructor import render_instructor_mode
from .student import render_student_mode

__all__ = [
    'render_instructor_mode',
    'render_student_mode'
]