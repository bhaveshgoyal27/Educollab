from config import get_openai_client, AGENT_MODEL
from typing import List, Dict, Any

class LearnerAgent:
    """
    Agent responsible for teaching concepts from slides with examples and numerical problems
    Adapts teaching based on student's weak areas identified by ReviewerAgent
    """
    
    def __init__(self):
        self.client = get_openai_client()
        self.conversation_history = []
    
    def teach_concept(self, 
                     slide_content: str, 
                     weak_areas: List[str] = None,
                     user_question: str = None) -> str:
        """
        Teach concepts from slides with focus on weak areas
        
        Args:
            slide_content: Content from the slides
            weak_areas: List of concepts student struggles with
            user_question: Optional specific question from student
        
        Returns:
            Teaching response with examples and explanations
        """
        
        system_prompt = self._get_system_prompt(weak_areas)
        
        # Build user message
        if user_question:
            user_message = f"""
            SLIDE CONTENT:
            {slide_content}
            
            STUDENT QUESTION:
            {user_question}
            
            Please provide a clear explanation with examples.
            """
        else:
            user_message = f"""
            SLIDE CONTENT:
            {slide_content}
            
            Please explain these concepts with:
            1. Clear, concise explanations
            2. Practical numerical examples
            3. Visual descriptions (when applicable)
            4. Real-world applications
            
            {"Focus especially on: " + ", ".join(weak_areas) if weak_areas else ""}
            """
        
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": user_message})
        
        try:
            response = self.client.chat.completions.create(
                model=AGENT_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt}
                ] + self.conversation_history,
                temperature=0.7,
                max_tokens=2000
            )
            
            assistant_message = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            
            # Keep conversation history manageable
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            return assistant_message
            
        except Exception as e:
            return f"Error in teaching: {str(e)}"
    
    def _get_system_prompt(self, weak_areas: List[str] = None) -> str:
        """Get system prompt for learner agent"""
        
        base_prompt = """You are an expert AI tutor who excels at explaining complex concepts clearly 
        and concisely. Your teaching style includes:
        
        1. Breaking down complex topics into digestible parts
        2. Using numerical examples and step-by-step solutions
        3. Providing real-world analogies and applications
        4. Creating visual descriptions when helpful (describe diagrams, flowcharts, etc.)
        5. Encouraging active learning through engagement
        
        Guidelines:
        - Be conversational and encouraging
        - Use concrete examples with numbers when teaching formulas or calculations
        - Explain WHY concepts work, not just HOW
        - Anticipate common misconceptions and address them
        - When describing visual concepts, be detailed and clear
        """
        
        if weak_areas:
            base_prompt += f"""
            
            IMPORTANT: The student has shown difficulty with these areas: {', '.join(weak_areas)}
            
            Pay special attention to these concepts:
            - Provide extra examples and practice problems
            - Break down these topics more thoroughly
            - Check for understanding more frequently
            - Offer different explanations or analogies
            """
        
        return base_prompt
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get current conversation history"""
        return self.conversation_history
