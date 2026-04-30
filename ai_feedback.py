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


def get_resume_feedback(resume_text: str) -> str:

    if not resume_text or len(resume_text.strip()) < 50:
        return "❌ Resume text is too short or empty to analyze."

    api_key = get_api_key()
    if not api_key:
        return "❌ API key not found. Check your secrets or .env file."

    client = Groq(api_key=api_key)

    prompt = (
        "You are a brutally honest resume reviewer and senior tech recruiter.\n"
        "You have high standards and you do NOT give inflated scores.\n\n"
        "SCORING RULES - follow these strictly:\n"
        "- 9.0 to 10.0 = Near perfect. Rare. Only for exceptional resumes.\n"
        "- 7.0 to 8.9 = Good but has clear gaps. Most resumes fall here.\n"
        "- 5.0 to 6.9 = Average. Missing metrics, weak summary, poor ATS.\n"
        "- 3.0 to 4.9 = Below average. Major issues with structure or clarity.\n"
        "- 1.0 to 2.9 = Poor. Needs complete rewrite.\n\n"
        "You MUST vary your score based on the actual quality of THIS resume.\n"
        "Do NOT default to 8.5. Evaluate honestly and critically.\n\n"
        "Analyze the resume and respond EXACTLY using these section headers:\n\n"
        "## ✅ Strengths\n"
        "- List exactly 4 specific strengths from THIS resume\n"
        "- Reference actual content, job titles, tools, or projects mentioned\n\n"
        "## 🔧 Areas for Improvement\n"
        "- List exactly 4 concrete improvements needed\n"
        "- Be direct, critical, and specific to THIS resume\n\n"
        "## 🔑 Missing Keywords\n"
        "- List exactly 6 keywords missing from THIS resume\n"
        "- Focus on ATS keywords relevant to the candidate target role\n\n"
        "## 💡 ATS Suggestions\n"
        "- List exactly 4 specific ATS formatting fixes for THIS resume\n\n"
        "## 🎯 Overall Score\n"
        "Score: X.X/10\n"
        "One honest sentence explaining exactly why this score was given.\n\n"
        "## 🔄 Before & After\n"
        "Find the single weakest bullet point in the work experience section.\n"
        "Rewrite it with strong action verbs, specific metrics, and clear impact.\n\n"
        "BEFORE:\n"
        "[copy the exact weak bullet point here]\n\n"
        "AFTER:\n"
        "[rewritten version with metrics and impact]\n\n"
        "Here is the resume to analyze:\n\n"
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
                        "Always respond with the exact section headers requested. "
                        "Never skip any section. Never give inflated scores."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.9,
            max_tokens=2000
        )
        return response.choices[0].message.content

    except Exception as e:
        return "❌ Groq API error: " + str(e)