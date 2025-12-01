# 📚 EduCanvas - AI-Powered Learning Platform

A comprehensive educational platform with AI-powered features for both instructors and students, built with Streamlit and OpenAI.

## 🌟 Features

### 👨‍🏫 Instructor Mode

1. **Slide Management**
   - Upload and organize course slides
   - Maintain slide order
   - Preview and manage uploaded content

2. **Quiz Creation**
   - **Manual Quiz Creation**: Create quizzes manually (placeholder)
   - **AI-Assisted Quiz Generation**:
     - Select specific slides for quiz content
     - Define learning objectives
     - Choose quiz type (MCQ, Conversational, Long Answer)
     - Review and modify AI-generated questions
     - Approve or regenerate quizzes

3. **Quiz Reports & Analytics**
   - View all student submissions
   - AI-powered grading with detailed feedback
   - Points breakdown (awarded/deducted)
   - Suggested improvements for student answers
   - Identification of strong and weak areas
   - Personalized recommendations

### 👨‍🎓 Student Mode

1. **Course & Slide Access**
   - Browse enrolled courses
   - View slides in order uploaded by instructor
   - Navigate through slides easily

2. **AI Study Companion (Learner Agent)**
   - Explains concepts from slides with clarity
   - Provides numerical examples and step-by-step solutions
   - Offers real-world applications and analogies
   - Describes visual concepts and diagrams
   - Adapts teaching based on student's weak areas
   - Interactive Q&A chat interface

3. **Practice Quizzes (Tester Agent)**
   - Generate practice questions on any topic
   - Choose difficulty level (Easy, Medium, Hard)
   - Focus on weak areas automatically
   - Instant feedback and explanations
   - Multiple question types

4. **Performance Review (Reviewer Agent)**
   - Analyzes quiz performance
   - Provides detailed feedback per question
   - Identifies weak areas and concepts to review
   - Suggests improvements for answers
   - Tracks learning progress
   - Communicates with Learner Agent for adaptive teaching
   - Only provides feedback if score < 90% threshold

## 🏗️ Project Structure

```
educanvas/
├── app.py                      # Main Streamlit application
├── config.py                   # Configuration and API settings
├── requirements.txt            # Python dependencies
├── README.md                   # Documentation
│
├── utils/
│   ├── __init__.py
│   ├── storage.py              # Data persistence management
│   └── ui_components.py        # Reusable UI components
│
├── agents/
│   ├── __init__.py
│   ├── quiz_generator.py       # AI quiz generation agent
│   ├── learner_agent.py        # AI tutor agent
│   ├── tester_agent.py         # Practice quiz agent
│   └── reviewer_agent.py       # Performance analysis agent
│
└── pages/
    ├── __init__.py
    ├── instructor.py            # Instructor mode interface
    └── student.py               # Student mode interface
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Installation

1. **Clone or create the project directory**
   ```bash
   mkdir educanvas
   cd educanvas
   ```

2. **Create the file structure**
   Create all the files as shown in the project structure above.

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Key**
   
   **Option 1: Environment Variable (Recommended)**
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```
   
   **Option 2: Direct Configuration**
   Edit `config.py` and replace the placeholder:
   ```python
   OPENAI_API_KEY = "your-api-key-here"
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Access the application**
   Open your browser and navigate to `http://localhost:8501`

## 📖 Usage Guide

### For Instructors

1. **Toggle to Instructor Mode** using the radio button in the top-right
2. **Select a Course** from the sidebar
3. **Upload Slides**: 
   - Go to "Manage Slides"
   - Upload PDF or image files
   - Slides are maintained in upload order
4. **Create AI Quiz**:
   - Go to "Create Quiz" → "AI-Assisted Quiz"
   - Select slides to include
   - Enter learning objectives
   - Choose quiz type and number of questions
   - Review generated questions
   - Modify or approve the quiz
5. **View Reports**:
   - Go to "Quiz Reports"
   - Select a quiz
   - View student submissions and AI grading
   - Review detailed feedback and analytics

### For Students

1. **Toggle to Student Mode** using the radio button
2. **Enter Your Name** in the sidebar
3. **Select a Course** from available courses
4. **View Slides**: Browse course materials in order
5. **Use AI Study Companion**:
   - Select a topic/slide
   - Click "Explain This Topic" for automatic teaching
   - Ask specific questions in the chat
   - Get personalized help on weak areas
6. **Practice with Quizzes**:
   - Generate practice questions
   - Choose difficulty and focus areas
   - Submit and get instant feedback
   - Review performance analysis
7. **Take Official Quizzes**:
   - Complete instructor-created quizzes
   - Receive detailed grading and feedback
   - Track your progress

## 🤖 AI Agent System

### Multi-Agent Architecture

1. **Quiz Generator Agent** (Instructor Tool)
   - Analyzes slide content and learning objectives
   - Generates pedagogically sound questions
   - Maps questions to cognitive levels
   - Provides rubrics and answer keys

2. **Learner Agent** (Student Tutor)
   - Teaches concepts from slides
   - Provides examples and numerical problems
   - Adapts to student's weak areas
   - Interactive conversational learning
   - Describes visual concepts

3. **Tester Agent** (Practice Quiz Generator)
   - Creates practice questions
   - Adjusts difficulty dynamically
   - Focuses on struggling areas
   - Prepares students for exams

4. **Reviewer Agent** (Performance Analyzer)
   - Grades student work with explanations
   - Identifies knowledge gaps
   - Provides actionable feedback
   - Triggers adaptive learning (< 90% threshold)
   - Communicates with Learner Agent

### Agent Communication Flow

```
Student Takes Quiz → Reviewer Agent Analyzes
                          ↓
                  Score < 90%?
                          ↓
                        YES
                          ↓
        Weak Areas Identified → Updated Student Profile
                          ↓
        Learner Agent Adapts → Focused Teaching
                          ↓
        Tester Agent Creates → Targeted Practice
```

## 🎨 Canvas-Like UI Features

- Clean, professional interface
- Card-based design for content
- Progress indicators with color coding
- Expandable sections for detailed content
- Responsive layout
- Chat-style interface for AI interactions
- Intuitive navigation

## ⚙️ Configuration Options

Edit `config.py` to customize:

- `DEFAULT_MODEL`: OpenAI model for general tasks
- `AGENT_MODEL`: Model for AI agents
- `QUIZ_TYPES`: Available quiz types
- `PASSING_THRESHOLD`: Score threshold for remediation (default: 90%)
- `DEFAULT_COURSES`: Pre-populated courses

## 📝 Notes

- **Data Persistence**: Currently uses Streamlit session state. For production, consider implementing database storage.
- **File Upload**: Slides are stored in session state. For production, implement proper file storage.
- **Authentication**: No authentication implemented. Add user auth for production use.
- **API Costs**: Monitor OpenAI API usage as agent calls can accumulate.

## 🔒 Security Considerations

- Keep your OpenAI API key secure
- Do not commit API keys to version control
- Use environment variables for production
- Implement proper user authentication
- Add rate limiting for API calls

## 🐛 Troubleshooting

**Issue**: "Module not found" errors
- **Solution**: Ensure all `__init__.py` files are created in subdirectories

**Issue**: API key not working
- **Solution**: Verify the key is correctly set in config.py or environment variables

**Issue**: Slides not displaying
- **Solution**: Check file format (PDF, PNG, JPG) and file size

**Issue**: Agent responses slow
- **Solution**: Normal for complex analysis. Consider using faster models for less critical tasks.

## 🚧 Future Enhancements

- [ ] Database integration for persistent storage
- [ ] User authentication and authorization
- [ ] Real-time collaboration features
- [ ] Advanced analytics dashboard
- [ ] Export reports to PDF
- [ ] Mobile-responsive improvements
- [ ] Multi-language support
- [ ] Video/audio slide support
- [ ] Discussion forums
- [ ] Calendar integration for quiz schedules

## 📄 License

This project is provided as-is for educational purposes.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 📧 Support

For questions or issues, please create an issue in the repository.

---

**Built with ❤️ using Streamlit and OpenAI**
