# 📄 AI Resume Feedback Tool

A web application that analyzes resumes using AI and provides structured, 
actionable feedback to help job seekers improve their chances.

---

## 🚀 Features

- Upload resume as **PDF or TXT**
- Automatic text extraction from PDF files
- AI-powered analysis using **LLaMA 3.3** via Groq API
- Structured feedback across 5 categories:
  - ✅ Strengths
  - 🔧 Areas for Improvement
  - 🔑 Missing Keywords
  - 💡 ATS Suggestions
  - 🎯 Overall Score
- Download feedback as a `.txt` file
- Clean, responsive UI built with Streamlit

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend/UI | Streamlit |
| PDF Extraction | pdfplumber |
| AI Model | LLaMA 3.3 70B (via Groq API) |
| Language | Python 3.10+ |
| Config | python-dotenv |

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/ai-resume-feedback.git
cd ai-resume-feedback
```

### 2. Create and activate virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your API key
- Get a free API key from [console.groq.com](https://console.groq.com)
- Create a `.env` file in the root folder: