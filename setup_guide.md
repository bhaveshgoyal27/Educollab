# 🚀 EduCanvas Quick Setup Guide

## Step-by-Step Setup

### 1. Create Project Structure

Create a new directory and organize files as follows:

```
educanvas/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── utils/
│   ├── __init__.py
│   ├── storage.py
│   └── ui_components.py
│
├── agents/
│   ├── __init__.py
│   ├── quiz_generator.py
│   ├── learner_agent.py
│   ├── tester_agent.py
│   └── reviewer_agent.py
│
└── pages/
    ├── __init__.py
    ├── instructor.py
    └── student.py
```

### 2. Copy Files

Copy each provided file to its corresponding location in the structure above.

### 3. Install Dependencies

```bash
cd educanvas
pip install -r requirements.txt
```

### 4. Configure OpenAI API Key

**Method 1: Environment Variable (Recommended for Security)**

**On macOS/Linux:**
```bash
export OPENAI_API_KEY='sk-your-actual-api-key-here'
```

**On Windows (Command Prompt):**
```cmd
set OPENAI_API_KEY=sk-your-actual-api-key-here
```

**On Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY='sk-your-actual-api-key-here'
```

**Method 2: Direct Configuration**

Open `config.py` and replace:
```python
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY_HERE"
```

with:
```python
OPENAI_API_KEY = "sk-your-actual-api-key-here"
```

### 5. Run the Application

```bash
streamlit run app.py
```

### 6. Access the Application

Open your browser and go to: `http://localhost:8501`

## 🎓 First Time Usage

### As an Instructor:

1. **Toggle to Instructor Mode** (top-right radio button)
2. **Select a Course** (e.g., "Introduction to Computer Science")
3. **Upload Slides**:
   - Navigate to "Manage Slides"
   - Click "Upload slides"
   - Select PDF or image files (PNG, JPG)
   - Click "Upload Slides"
4. **Create Your First Quiz**:
   - Go to "Create Quiz" → "AI-Assisted Quiz" tab
   - Enter a quiz title (e.g., "Week 1 Quiz")
   - Select quiz type (try "Multiple Choice (MCQ)")
   - Select which slides to include
   - Enter learning objectives (e.g., "Understand basic data structures")
   - Click "Generate Quiz"
   - Review the generated questions
   - Click "Approve & Publish Quiz"

### As a Student:

1. **Toggle to Student Mode**
2. **Enter Your Name** (in the sidebar)
3. **Select a Course**
4. **View Slides**:
   - Go to "View Slides"
   - Navigate through uploaded slides
5. **Try AI Study Companion**:
   - Go to "AI Study Companion"
   - Select a slide/topic
   - Click "Explain This Topic"
   - Ask questions in the chat
6. **Practice Quizzes**:
   - Go to "Practice Quizzes"
   - Select a topic and difficulty
   - Click "Generate Practice Quiz"
   - Answer questions and submit
   - Review detailed feedback
7. **Take Official Quiz**:
   - Go to "Take Quiz"
   - Select an available quiz
   - Complete and submit
   - View your results and feedback

## 📋 Checklist

- [ ] All files created in correct structure
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] OpenAI API key configured
- [ ] Application runs without errors (`streamlit run app.py`)
- [ ] Can toggle between Instructor and Student modes
- [ ] Can upload slides (Instructor mode)
- [ ] Can generate AI quiz (Instructor mode)
- [ ] Can view slides (Student mode)
- [ ] AI Study Companion works (Student mode)
- [ ] Practice quizzes generate (Student mode)

## ⚠️ Common Issues

### Issue: ModuleNotFoundError
**Solution**: Ensure you have `__init__.py` files in all subdirectories:
- `utils/__init__.py`
- `agents/__init__.py`
- `pages/__init__.py`

### Issue: OpenAI API Error
**Solution**: 
1. Verify your API key is correct
2. Check you have credits in your OpenAI account
3. Ensure no extra spaces in the API key

### Issue: Slides Not Uploading
**Solution**:
1. Check file format (must be PDF, PNG, or JPG)
2. Ensure file size is reasonable (< 10MB)
3. Check console for error messages

### Issue: Streamlit Not Found
**Solution**:
```bash
pip install streamlit --upgrade
```

## 🎯 Testing the Multi-Agent System

### Test the Full Agent Workflow:

1. **As Student**: Take a practice quiz and score < 90%
2. **Check**: Weak areas should be identified
3. **Go to AI Study Companion**: It should focus on those weak areas
4. **Take Another Practice Quiz**: Questions should focus on weak areas
5. **Improve Performance**: Score > 90% to stop remediation

### Test Agent Communication:

```
[Student Performance < 90%]
       ↓
[Reviewer Agent Identifies Weak Areas]
       ↓
[Student Profile Updated]
       ↓
[Learner Agent Adapts Teaching]
       ↓
[Tester Agent Creates Focused Practice]
       ↓
[Student Improves → Cycle Stops at 90%+]
```

## 🔧 Configuration Tips

### Adjust AI Behavior:

In `config.py`, you can modify:

```python
# Use different models
DEFAULT_MODEL = "gpt-4o-mini"  # Faster, cheaper
AGENT_MODEL = "gpt-4o"  # More capable

# Change passing threshold
PASSING_THRESHOLD = 80  # Lower threshold for more lenient grading

# Add more courses
DEFAULT_COURSES = [
    "Introduction to Computer Science",
    "Data Structures",
    "Machine Learning",
    "Your Custom Course"
]
```

## 📊 Monitoring Usage

Track your OpenAI API usage at: https://platform.openai.com/usage

**Typical Costs (approximate):**
- Quiz Generation (5 questions): ~$0.05-0.10
- Study Companion conversation: ~$0.01-0.03 per message
- Practice Quiz (5 questions): ~$0.05-0.10
- Quiz Grading: ~$0.02-0.05 per submission

## 🎨 Customization Ideas

1. **Custom Branding**: Modify CSS in `config.py`
2. **Add Course Categories**: Extend `DEFAULT_COURSES`
3. **Different Quiz Types**: Add to `QUIZ_TYPES`
4. **Adjust Agent Prompts**: Modify system prompts in agent files
5. **Custom UI Components**: Add to `ui_components.py`

## 🚀 Next Steps

1. ✅ Complete the checklist above
2. 📚 Read the full README.md for detailed features
3. 🧪 Test all features in both modes
4. 🎓 Create your first complete course with slides and quizzes
5. 💡 Customize the application for your needs

## 💬 Getting Help

If you encounter issues:
1. Check the error message in the terminal
2. Review this guide and README.md
3. Verify all files are in correct locations
4. Check OpenAI API key and credits
5. Try with a fresh installation

## 🎉 You're Ready!

Once you've completed the setup, you have a fully functional AI-powered educational platform with:
- ✅ Intelligent quiz generation
- ✅ Adaptive AI tutoring
- ✅ Automated grading with feedback
- ✅ Multi-agent learning system
- ✅ Canvas-like professional UI

**Happy Teaching and Learning! 📚🎓**
