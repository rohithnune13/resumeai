# ai_feedback.py

import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


def get_api_key():
    try:
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        pass
    key = os.getenv("GROQ_API_KEY")
    if key:
        return key
    return None


def is_resume(text: str) -> bool:
    resume_keywords = [
        "experience", "education", "skills", "work",
        "project", "internship", "university", "college",
        "bachelor", "master", "engineer", "developer",
        "manager", "analyst", "certification", "volunteer",
        "summary", "objective", "employment", "responsibilities"
    ]
    text_lower = text.lower()
    matches = sum(1 for kw in resume_keywords if kw in text_lower)
    return matches >= 3


def get_resume_feedback(resume_text: str) -> str:

    if not resume_text or len(resume_text.strip()) < 50:
        return "❌ Resume text is too short or empty to analyze."

    if not is_resume(resume_text):
        return (
            "❌ This document does not appear to be a resume. "
            "Please upload a valid resume in PDF or TXT format. "
            "Make sure it includes sections like Experience, "
            "Education, and Skills."
        )

    api_key = get_api_key()
    if not api_key:
        return "❌ API key not found. Check your secrets or .env file."

    client = Groq(api_key=api_key)

    prompt = (
        "Analyze this resume and provide qualitative feedback only.\n"
        "Do NOT include a score — the score is calculated separately.\n\n"
        "Respond EXACTLY using these section headers:\n\n"
        "## ✅ Strengths\n"
        "- List exactly 4 specific strengths referencing actual content\n\n"
        "## 🔧 Areas for Improvement\n"
        "- List exactly 4 critical improvements with specific examples\n\n"
        "## 🔑 Missing Keywords\n"
        "- List exactly 6 missing ATS keywords for this candidate role\n\n"
        "## 💡 ATS Suggestions\n"
        "- List exactly 4 specific formatting fixes\n\n"
        "## 🎯 Overall Score\n"
        "One honest sentence summarizing the resume quality.\n\n"
        "## 🔄 Before & After\n"
        "Find the weakest bullet point. Rewrite it with metrics and impact.\n\n"
        "BEFORE:\n"
        "[exact weak bullet point]\n\n"
        "AFTER:\n"
        "[rewritten with metrics]\n\n"
        "Resume to analyze:\n\n"
        + resume_text
    )

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert resume reviewer. "
                        "Always respond with exact section headers. "
                        "Never skip sections. Be specific and reference "
                        "actual content from the resume."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content

    except Exception as e:
        return "❌ Groq API error: " + str(e)