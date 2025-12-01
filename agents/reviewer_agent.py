from config import get_openai_client, AGENT_MODEL, PASSING_THRESHOLD
from typing import List, Dict, Any
import json

class ReviewerAgent:
    """
    Agent responsible for analyzing student quiz performance and providing feedback
    Identifies weak areas and communicates with LearnerAgent for adaptive teaching
    """
    
    def __init__(self):
        self.client = get_openai_client()
    
    def analyze_quiz_performance(self,
                                quiz_questions: List[Dict[str, Any]],
                                student_answers: List[Dict[str, Any]],
                                quiz_type: str) -> Dict[str, Any]:
        """
        Analyze student's quiz performance and provide detailed feedback
        
        Args:
            quiz_questions: List of quiz questions with correct answers
            student_answers: Student's answers to the questions
            quiz_type: Type of quiz (MCQ, Conversational, Long Answer)
        
        Returns:
            Analysis with score, feedback, weak areas, and recommendations
        """
        
        system_prompt = self._get_system_prompt(quiz_type)
        user_prompt = self._build_analysis_prompt(quiz_questions, student_answers)
        
        try:
            response = self.client.chat.completions.create(
                model=AGENT_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,  # Lower temperature for consistent grading
                response_format={"type": "json_object"}
            )
            
            analysis = json.loads(response.choices[0].message.content)
            
            # Determine if feedback should be sent to learner agent
            overall_score = analysis.get('overall_score', 0)
            analysis['needs_remediation'] = overall_score < PASSING_THRESHOLD
            
            return analysis
            
        except Exception as e:
            return {
                "error": f"Failed to analyze performance: {str(e)}",
                "overall_score": 0,
                "needs_remediation": True
            }
    
    def grade_individual_answer(self,
                               question: Dict[str, Any],
                               student_answer: str,
                               max_points: int = 10) -> Dict[str, Any]:
        """
        Grade a single answer with detailed feedback
        
        Args:
            question: Question details including correct answer/rubric
            student_answer: Student's answer
            max_points: Maximum points for this question
        
        Returns:
            Grading details with points, feedback, and improvements
        """
        
        prompt = f"""Grade this answer and provide detailed feedback:
        
        QUESTION:
        {question.get('question', '')}
        
        CORRECT ANSWER/RUBRIC:
        {json.dumps(question.get('correct_answer') or question.get('rubric'), indent=2)}
        
        STUDENT ANSWER:
        {student_answer}
        
        Maximum Points: {max_points}
        
        Provide grading in JSON format:
        {{
            "points_earned": <number>,
            "max_points": {max_points},
            "percentage": <percentage>,
            "feedback": {{
                "strengths": ["What the student did well"],
                "weaknesses": ["What was missing or incorrect"],
                "points_awarded_for": ["Specific aspects that earned points"],
                "points_deducted_for": ["Specific aspects that lost points"]
            }},
            "suggested_answer": "An improved version of the answer",
            "concepts_to_review": ["Specific concepts to study"]
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=AGENT_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            return {
                "error": f"Grading failed: {str(e)}",
                "points_earned": 0,
                "max_points": max_points
            }
    
    def generate_summary_report(self, analysis: Dict[str, Any]) -> str:
        """
        Generate a comprehensive summary report for the student
        
        Args:
            analysis: Complete analysis from analyze_quiz_performance
        
        Returns:
            Human-readable summary report
        """
        
        overall_score = analysis.get('overall_score', 0)
        weak_areas = analysis.get('weak_areas', [])
        strong_areas = analysis.get('strong_areas', [])
        recommendations = analysis.get('recommendations', [])
        
        report = f"""
        📊 **Quiz Performance Summary**
        
        **Overall Score:** {overall_score:.1f}%
        
        """
        
        if strong_areas:
            report += f"""
        ✅ **Strengths:**
        {chr(10).join(f"  • {area}" for area in strong_areas)}
        
        """
        
        if weak_areas:
            report += f"""
        ⚠️ **Areas for Improvement:**
        {chr(10).join(f"  • {area}" for area in weak_areas)}
        
        """
        
        if recommendations:
            report += f"""
        💡 **Recommendations:**
        {chr(10).join(f"  {i+1}. {rec}" for i, rec in enumerate(recommendations))}
        """
        
        if overall_score < PASSING_THRESHOLD:
            report += f"""
        
        📚 **Next Steps:**
        Your AI tutor will focus on the areas identified above in future sessions. 
        Practice more with the Quiz Tester agent to improve your understanding.
        """
        
        return report
    
    def _get_system_prompt(self, quiz_type: str) -> str:
        """Get system prompt for reviewer agent"""
        
        return f"""You are an expert educational evaluator and learning analytics specialist.
        Your role is to:
        
        1. Fairly and consistently grade student answers
        2. Provide constructive, actionable feedback
        3. Identify specific knowledge gaps and weak areas
        4. Suggest targeted improvements
        5. Recognize strengths and good understanding
        
        Quiz Type: {quiz_type}
        
        Grading Principles:
        - Be fair but rigorous
        - Partial credit for partially correct answers
        - Clear explanation of why points were awarded or deducted
        - Focus on understanding, not just correctness
        - Identify misconceptions, not just errors
        
        Return analysis in JSON format with:
        {{
            "overall_score": <percentage>,
            "question_scores": [
                {{
                    "question_number": 1,
                    "points_earned": <number>,
                    "max_points": <number>,
                    "feedback": "Detailed feedback"
                }}
            ],
            "weak_areas": ["Specific concepts to review"],
            "strong_areas": ["Concepts well understood"],
            "recommendations": ["Specific study recommendations"],
            "overall_feedback": "Summary of performance"
        }}
        """
    
    def _build_analysis_prompt(self, questions: List[Dict], answers: List[Dict]) -> str:
        """Build prompt for quiz analysis"""
        
        prompt = "Analyze this quiz submission:\n\n"
        
        for i, (q, a) in enumerate(zip(questions, answers), 1):
            prompt += f"""
        QUESTION {i}:
        {q.get('question', '')}
        Correct Answer: {q.get('correct_answer') or q.get('sample_answer', 'See rubric')}
        
        STUDENT ANSWER {i}:
        {a.get('answer', 'No answer provided')}
        
        ---
        """
        
        prompt += """
        Provide comprehensive analysis with:
        1. Individual question scores and feedback
        2. Overall performance score
        3. Identified weak areas (specific concepts)
        4. Strong areas
        5. Actionable recommendations for improvement
        """
        
        return prompt
