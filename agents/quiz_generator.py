from config import get_openai_client, DEFAULT_MODEL
from typing import List, Dict, Any
import json

class QuizGeneratorAgent:
    """Agent responsible for generating quizzes based on learning objectives"""
    
    def __init__(self):
        self.client = get_openai_client()
    
    def generate_quiz(self, 
                     slide_content: str, 
                     learning_objectives: str, 
                     quiz_type: str,
                     num_questions: int = 5) -> Dict[str, Any]:
        """
        Generate a quiz based on slide content and learning objectives
        
        Args:
            slide_content: Content from selected slides
            learning_objectives: Instructor's learning objectives
            quiz_type: Type of quiz (MCQ, Conversational, Long Answer)
            num_questions: Number of questions to generate
        
        Returns:
            Dictionary containing quiz questions with objectives
        """
        
        system_prompt = self._get_system_prompt(quiz_type)
        user_prompt = self._build_user_prompt(slide_content, learning_objectives, num_questions)
        
        try:
            response = self.client.chat.completions.create(
                model=DEFAULT_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            quiz_data = json.loads(response.choices[0].message.content)
            return quiz_data
            
        except Exception as e:
            return {
                "error": f"Failed to generate quiz: {str(e)}",
                "questions": []
            }
    
    def _get_system_prompt(self, quiz_type: str) -> str:
        """Get system prompt based on quiz type"""
        
        base_prompt = """You are an expert educational assessment designer. Your task is to create 
        high-quality, pedagogically sound quiz questions that align with specific learning objectives.
        
        For each question, you must provide:
        1. The question text
        2. The specific learning objective it addresses
        3. The cognitive level (Remember, Understand, Apply, Analyze, Evaluate, Create)
        """
        
        if quiz_type == "Multiple Choice (MCQ)":
            return base_prompt + """
            
            Create multiple-choice questions with:
            - 4 answer options (A, B, C, D)
            - Only one correct answer
            - Plausible distractors that test common misconceptions
            - Clear, unambiguous wording
            
            Return JSON format:
            {
                "questions": [
                    {
                        "question": "Question text",
                        "options": ["A. Option 1", "B. Option 2", "C. Option 3", "D. Option 4"],
                        "correct_answer": "A",
                        "learning_objective": "Specific objective this tests",
                        "cognitive_level": "Apply",
                        "explanation": "Why this is the correct answer"
                    }
                ]
            }
            """
        
        elif quiz_type == "Conversational":
            return base_prompt + """
            
            Create open-ended conversational questions that:
            - Encourage critical thinking and discussion
            - Allow for multiple valid approaches
            - Test deep understanding rather than memorization
            
            Return JSON format:
            {
                "questions": [
                    {
                        "question": "Question text",
                        "learning_objective": "Specific objective this tests",
                        "cognitive_level": "Analyze",
                        "sample_answer": "Example of a good response",
                        "key_points": ["Point 1", "Point 2"]
                    }
                ]
            }
            """
        
        else:  # Long Answer
            return base_prompt + """
            
            Create long-answer questions that:
            - Require detailed, structured responses
            - Test comprehensive understanding
            - Include specific rubric criteria
            
            Return JSON format:
            {
                "questions": [
                    {
                        "question": "Question text",
                        "learning_objective": "Specific objective this tests",
                        "cognitive_level": "Evaluate",
                        "rubric": {
                            "excellent": "Criteria for excellent answer",
                            "good": "Criteria for good answer",
                            "needs_improvement": "Criteria for needs improvement"
                        },
                        "expected_length": "2-3 paragraphs"
                    }
                ]
            }
            """
    
    def _build_user_prompt(self, slide_content: str, learning_objectives: str, num_questions: int) -> str:
        """Build user prompt with content and objectives"""
        return f"""
        Based on the following slide content and learning objectives, generate {num_questions} quiz questions.
        
        SLIDE CONTENT:
        {slide_content}
        
        LEARNING OBJECTIVES:
        {learning_objectives}
        
        Ensure each question directly maps to a learning objective and tests the appropriate cognitive level.
        """
