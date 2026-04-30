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
        "Analyze this resume and score it STRICTLY based on these criteria:\n\n"
        "STEP 1 - Check these elements and note what is present or missing:\n"
        "[ ] Does it have quantified achievements? (numbers, percentages, impact)\n"
        "[ ] Does it have a strong specific summary? (not generic)\n"
        "[ ] Does it have relevant ATS keywords for the target role?\n"
        "[ ] Does it have clean consistent formatting?\n"
        "[ ] Does it show career progression?\n"
        "[ ] Are bullet points action-verb led?\n\n"
        "STEP 2 - Score based on how many boxes are checked:\n"
        "6 checked = 9.0 to 10.0\n"
        "5 checked = 8.0 to 8.9\n"
        "4 checked = 7.0 to 7.9\n"
        "3 checked = 5.5 to 6.9\n"
        "2 checked = 4.0 to 5.4\n"
        "1 or 0 checked = 1.0 to 3.9\n\n"
        "STEP 3 - Respond EXACTLY using these section headers:\n\n"
        "## ✅ Strengths\n"
        "- List exactly 4 specific strengths referencing actual content\n\n"
        "## 🔧 Areas for Improvement\n"
        "- List exactly 4 critical improvements with specific examples\n\n"
        "## 🔑 Missing Keywords\n"
        "- List exactly 6 missing ATS keywords for this candidate role\n\n"
        "## 💡 ATS Suggestions\n"
        "- List exactly 4 specific formatting fixes\n\n"
        "## 🎯 Overall Score\n"
        "Score: X.X/10\n"
        "Checked boxes: X out of 6\n"
        "One sentence explaining the score.\n\n"
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
                        "You are a harsh but fair senior technical recruiter "
                        "at a top tech company. You review hundreds of resumes "
                        "weekly. You are known for giving VERY different scores "
                        "to different resumes. "
                        "A resume with no metrics gets maximum 6.0. "
                        "A resume with vague bullet points gets maximum 5.5. "
                        "A resume with quantified achievements, clean ATS "
                        "formatting, and relevant keywords can score 8.5 or above. "
                        "Always respond with exact section headers. "
                        "Never skip sections."
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