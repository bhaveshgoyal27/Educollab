# pages/__init__.py
"""Page modules for EduCanvas application"""

from .instructor import render_instructor_mode
from .student import render_student_mode

__all__ = [
    'render_instructor_mode',
    'render_student_mode'
]