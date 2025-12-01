# 🏗️ EduCanvas System Architecture

## Overview

EduCanvas is a multi-agent educational platform built on Streamlit with OpenAI-powered intelligent agents. The system uses a modular architecture with clear separation between UI, business logic, and AI agents.

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      Streamlit Frontend                      │
│  ┌───────────────────────┐  ┌───────────────────────────┐  │
│  │   Instructor Mode     │  │      Student Mode         │  │
│  │  - Slide Management   │  │  - View Slides            │  │
│  │  - Quiz Creation      │  │  - AI Study Companion     │  │
│  │  - Reports/Analytics  │  │  - Practice Quizzes       │  │
│  │                       │  │  - Take Official Quizzes  │  │
│  └───────────────────────┘  └───────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                   Storage Layer (Session State)              │
│  - Courses & Slides                                          │
│  - Quizzes & Questions                                       │
│  - Student Attempts & Progress                               │
│  - Agent Conversation History                                │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                        AI Agent Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │Quiz Generator│  │Learner Agent │  │Tester Agent  │      │
│  │   Agent      │  │  (Tutor)     │  │  (Practice)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         ↕                  ↕                  ↕              │
│  ┌────────────────────────────────────────────────────┐    │
│  │          Reviewer Agent (Performance Analysis)      │    │
│  │  - Grades submissions                               │    │
│  │  - Identifies weak areas                            │    │
│  │  - Triggers adaptive learning                       │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                      OpenAI API (GPT-4)                      │
└─────────────────────────────────────────────────────────────┘
```

## Component Breakdown

### 1. Frontend Layer (Streamlit)

#### Main Components:
- **app.py**: Entry point, mode toggle, navigation
- **pages/instructor.py**: Instructor interface
- **pages/student.py**: Student interface

#### Features:
- Canvas-like UI design
- Real-time updates via Streamlit's reactivity
- File upload handling
- Interactive forms and inputs
- Chat interfaces for AI interactions

### 2. Storage Layer

#### Implementation:
- Uses Streamlit Session State (in-memory)
- Organized storage modules in `utils/storage.py`

#### Data Models:

**Courses**
```python
{
    'name': str,
    'id': str
}
```

**Slides**
```python
{
    'id': str,
    'title': str,
    'file': bytes,
    'order': int,
    'content': str
}
```

**Quizzes**
```python
{
    'id': str,
    'title': str,
    'type': str,
    'learning_objectives': str,
    'questions': [
        {
            'question': str,
            'options': List[str],  # for MCQ
            'correct_answer': str,
            'learning_objective': str,
            'cognitive_level': str,
            'explanation': str
        }
    ],
    'created_at': str
}
```

**Student Progress**
```python
{
    'weak_areas': List[str],
    'quiz_history': List[dict],
    'learning_context': str
}
```

### 3. AI Agent Layer

#### Agent Architecture

Each agent is a self-contained class with:
- OpenAI client initialization
- Specialized system prompts
- Input/output processing
- Error handling

#### Agent Details:

**1. Quiz Generator Agent**
```
Purpose: Generate quizzes from slides and learning objectives
Input: Slide content, learning objectives, quiz type
Output: Structured quiz with questions, answers, rubrics
Model: GPT-4o
Temperature: 0.7 (creative but consistent)
```

**2. Learner Agent (Tutor)**
```
Purpose: Teach concepts interactively with adaptation
Input: Slide content, weak areas, user questions
Output: Explanations, examples, numerical problems
Model: GPT-4o
Temperature: 0.7
Features: 
  - Conversation history management
  - Adaptive teaching based on weak areas
  - Visual concept descriptions
```

**3. Tester Agent**
```
Purpose: Generate practice questions for exam prep
Input: Topics, difficulty level, focus areas
Output: Practice questions with answers and explanations
Model: GPT-4o
Temperature: 0.8 (more creative for variety)
```

**4. Reviewer Agent**
```
Purpose: Grade work and provide detailed feedback
Input: Questions, student answers, quiz type
Output: Scores, feedback, weak areas, recommendations
Model: GPT-4o
Temperature: 0.3 (consistent grading)
Features:
  - Detailed rubric-based grading
  - Identifies knowledge gaps
  - Triggers adaptive learning loop
```

## Multi-Agent Communication Flow

### Adaptive Learning Loop

```
┌─────────────────────────────────────────────────────────────┐
│ STEP 1: Student Takes Quiz/Practice                         │
│   - Answers questions                                        │
│   - Submits for grading                                      │
└──────────────────────────┬──────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 2: Reviewer Agent Analyzes                             │
│   - Grades each answer                                       │
│   - Calculates overall score                                 │
│   - Identifies specific weak areas                           │
│   - Generates detailed feedback                              │
└──────────────────────────┬──────────────────────────────────┘
                           ↓
                    Score < 90%?
                           ↓
                         YES
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 3: Update Student Profile                              │
│   - Add weak areas to profile                                │
│   - Update learning context                                  │
│   - Trigger remediation flag                                 │
└──────────────────────────┬──────────────────────────────────┘
                           ↓
         ┌─────────────────┴─────────────────┐
         ↓                                     ↓
┌─────────────────────┐           ┌─────────────────────┐
│ STEP 4A:            │           │ STEP 4B:            │
│ Learner Agent       │           │ Tester Agent        │
│ Adapts Teaching     │           │ Creates Focused     │
│                     │           │ Practice            │
│ - Reads weak areas  │           │                     │
│ - Focuses teaching  │           │ - Targets weak      │
│ - Extra examples    │           │   areas             │
│ - Different angles  │           │ - Appropriate       │
│                     │           │   difficulty        │
└─────────────────────┘           └─────────────────────┘
         ↓                                     ↓
         └─────────────────┬─────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 5: Student Continues Learning                          │
│   - Studies with adapted tutor                               │
│   - Practices with focused quizzes                           │
│   - Takes another quiz                                       │
│   - Loop continues until score >= 90%                        │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow Examples

### Example 1: AI Quiz Generation Flow

```
Instructor Action:
1. Selects slides (e.g., Slides 1-3)
2. Enters objectives: "Understand sorting algorithms"
3. Chooses MCQ, 5 questions

     ↓
Quiz Generator Agent:
1. Analyzes slide content
2. Maps to learning objectives
3. Generates questions at appropriate cognitive levels
4. Creates answer keys and explanations

     ↓
Review Interface:
1. Shows all generated questions
2. Instructor can modify/remove
3. Approve → Saves to storage
```

### Example 2: Student Learning Flow

```
Student Action:
1. Opens AI Study Companion
2. Selects "Data Structures" slide

     ↓
System Check:
- Retrieves student progress
- Finds weak area: "Binary Trees"

     ↓
Learner Agent:
1. Receives slide content
2. Receives weak area flag
3. Generates explanation with:
   - Extra focus on binary trees
   - Multiple examples
   - Step-by-step walkthroughs
   - Visual descriptions

     ↓
Student Interaction:
- Reads explanation
- Asks follow-up question
- Gets clarification
- Improved understanding
```

### Example 3: Practice Quiz Feedback Loop

```
Student:
Takes practice quiz on "Algorithms"
Scores 75% (below threshold)

     ↓
Reviewer Agent:
1. Grades each answer
2. Identifies weak concepts:
   - Time complexity analysis
   - Space-time tradeoffs
3. Provides detailed feedback

     ↓
Storage Update:
Student profile updated:
weak_areas: ["time complexity", "space-time tradeoffs"]

     ↓
Next Study Session:
Learner Agent automatically:
- Focuses on time complexity
- Provides numerical examples
- Extra practice problems

     ↓
Next Practice Quiz:
Tester Agent:
- Includes more questions on weak areas
- Tests understanding improvements

     ↓
Student Improvement:
Takes another quiz, scores 92%
Weak areas removed from profile
```

## Technology Stack

### Core Technologies
- **Streamlit**: Frontend framework
- **OpenAI API**: AI model access (GPT-4)
- **Python 3.8+**: Backend language

### Key Libraries
- **openai**: Official OpenAI Python client
- **streamlit**: Web app framework
- **Pillow**: Image processing
- **python-dotenv**: Environment management

## Scalability Considerations

### Current Limitations
- **Storage**: Session-based (ephemeral)
- **Concurrency**: Single-user sessions
- **File Storage**: In-memory only

### Production Recommendations

1. **Database Layer**
```
Replace Session State with:
- PostgreSQL for structured data
- MongoDB for flexible documents
- Redis for session management
```

2. **File Storage**
```
Implement:
- AWS S3 for slide storage
- CloudFlare for CDN
- Thumbnail generation
```

3. **Authentication**
```
Add:
- OAuth 2.0 integration
- Role-based access control
- Session management
```

4. **API Optimization**
```
Implement:
- Response caching
- Rate limiting
- Async processing
- Background jobs for grading
```

5. **Monitoring**
```
Add:
- Application logging
- Performance metrics
- API usage tracking
- Error monitoring (Sentry)
```

## Security Considerations

### Current Implementation
- API keys in environment variables
- No user data persistence
- Session-based isolation

### Production Requirements
- Encrypted database connections
- Secure file upload validation
- Input sanitization
- Rate limiting
- API key rotation
- Audit logging

## Performance Optimization

### Agent Response Time
- **Quiz Generation**: 5-15 seconds
- **Teaching Response**: 3-10 seconds
- **Grading**: 3-8 seconds per question

### Optimization Strategies
1. Use faster models for non-critical tasks
2. Implement caching for repeated queries
3. Stream responses for better UX
4. Batch processing for multiple items
5. Async processing for background tasks

## Extension Points

### Easy Customizations
1. Add new quiz types in `config.py`
2. Modify agent prompts for different teaching styles
3. Add custom UI components
4. Extend storage models
5. Create new agent types

### Advanced Extensions
1. Multi-modal learning (video, audio)
2. Collaborative features (peer review)
3. Analytics dashboard
4. Mobile app
5. Integration with LMS platforms

## Testing Strategy

### Unit Tests
- Agent prompt generation
- Storage operations
- UI component rendering

### Integration Tests
- End-to-end quiz creation
- Student learning workflow
- Agent communication

### User Acceptance Tests
- Instructor workflows
- Student learning paths
- AI response quality

---

**This architecture provides a solid foundation for an AI-powered educational platform with room for growth and customization.**
