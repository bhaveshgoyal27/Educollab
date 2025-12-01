from config import get_openai_client, AGENT_MODEL
from typing import List, Dict, Any
import json

class TesterAgent:
    """
    Agent responsible for creating practice quizzes and test questions
    to help students prepare for exams
    """
    
    def __init__(self):
        self.client = get_openai_client()
    
    def generate_practice_quiz(self,
                              slide_content: str,
                              difficulty_level: str = "Medium",
                              num_questions: int = 5,
                              focus_areas: List[str] = None) -> Dict[str, Any]:
        """
        Generate practice quiz questions
        
        Args:
            slide_content: Content from slides to base questions on
            difficulty_level: Easy, Medium, or Hard
            num_questions: Number of questions to generate
            focus_areas: Specific topics to focus on
        
        Returns:
            Dictionary with practice questions
        """
        
        system_prompt = self._get_system_prompt(difficulty_level)
        user_prompt = self._build_prompt(slide_content, num_questions, focus_areas)
        
        try:
            response = self.client.chat.completions.create(
                model=AGENT_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.8,
                response_format={"type": "json_object"}
            )
            
            quiz_data = json.loads(response.choices[0].message.content)
            return quiz_data
            
        except Exception as e:
            return {
                "error": f"Failed to generate practice quiz: {str(e)}",
                "questions": []
            }
    
    def generate_quick_question(self, topic: str) -> Dict[str, Any]:
        """
        Generate a single quick practice question on a specific topic
        
        Args:
            topic: Specific topic or concept to test
        
        Returns:
            Single question with answer
        """
        
        prompt = f"""Generate one practice question on the topic: {topic}
        
        Make it a thought-provoking question that tests understanding, not just memorization.
        Include the answer and a brief explanation.
        
        Return in JSON format:
        {{
            "question": "Question text",
            "answer": "Detailed answer",
            "explanation": "Why this answer is correct",
            "hints": ["Hint 1", "Hint 2"]
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=AGENT_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            return {"error": f"Failed to generate question: {str(e)}"}
    
    def _get_system_prompt(self, difficulty_level: str) -> str:
        """Get system prompt based on difficulty level"""
        
        difficulty_guidance = {
            "Easy": """
            - Focus on fundamental concepts and definitions
            - Use straightforward scenarios
            - Test basic recall and understanding
            """,
            "Medium": """
            - Mix conceptual understanding with application
            - Include problem-solving scenarios
            - Test ability to connect different concepts
            """,
            "Hard": """
            - Focus on advanced application and analysis
            - Include complex multi-step problems
            - Test critical thinking and synthesis
            - Challenge common assumptions
            """
        }
        
        return f"""You are an expert educational test designer creating practice questions 
        to help students prepare for exams. 
        
        Difficulty Level: {difficulty_level}
        {difficulty_guidance.get(difficulty_level, difficulty_guidance["Medium"])}
        
        Create questions that:
        1. Test deep understanding, not just memorization
        2. Include clear, unambiguous wording
        3. Provide detailed answers with explanations
        4. Cover various cognitive levels (Remember, Understand, Apply, Analyze)
        5. Include practical examples when applicable
        
        Return questions in JSON format:
        {{
            "questions": [
                {{
                    "question": "Question text",
                    "type": "MCQ or Short Answer or Problem Solving",
                    "options": ["A. ", "B. ", "C. ", "D. "] (for MCQ only),
                    "correct_answer": "Answer",
                    "explanation": "Detailed explanation",
                    "difficulty": "Easy/Medium/Hard",
                    "topic": "Specific topic covered"
                }}
            ]
        }}
        """
    
    def _build_prompt(self, slide_content: str, num_questions: int, focus_areas: List[str]) -> str:
        """Build user prompt for quiz generation"""
        
        prompt = f"""Generate {num_questions} practice questions based on this content:
        
        CONTENT:
        {slide_content}
        """
        
        if focus_areas:
            prompt += f"""
            
            FOCUS AREAS (prioritize questions on these topics):
            {', '.join(focus_areas)}
            """
        
        prompt += """
        
        Create a mix of question types (MCQ, short answer, problem-solving) that would 
        effectively prepare a student for an exam on this material.
        """
        
        return prompt
