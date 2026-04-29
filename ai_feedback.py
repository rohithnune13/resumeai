# ai_feedback.py
# Upgraded prompt — returns feedback + before/after rewrite in one call

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


def get_resume_feedback(resume_text: str) -> str:
    """
    Sends resume to Groq LLaMA and returns structured feedback
    including a before/after bullet point rewrite.
    """
    if not resume_text or len(resume_text.strip()) < 50:
        return "❌ Resume text is too short or empty to analyze."

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "❌ API key not found. Check your .env file."

    client = Groq(api_key=api_key)

    prompt = f"""
You are an expert resume reviewer and career coach with 10+ years of experience
in tech hiring. Analyze the resume below and provide clear, honest, structured feedback.

Format your response EXACTLY using these section headers — do not change them:

## ✅ Strengths
- List exactly 4 specific strengths from this resume
- Be specific, reference actual content from the resume

## 🔧 Areas for Improvement
- List exactly 4 concrete things to fix
- Be direct and actionable

## 🔑 Missing Keywords
- List exactly 6 important keywords missing from this resume
- Focus on keywords ATS systems and recruiters look for

## 💡 ATS Suggestions
- List exactly 4 specific ATS formatting tips for this resume

## 🎯 Overall Score
Give a score in this exact format: X.X/10
Then one sentence explaining the score.

## 🔄 Before & After
Find the single weakest bullet point in the resume work experience.
Then rewrite it to be stronger with metrics and impact.

BEFORE:
[paste the exact weak bullet point from the resume here]

AFTER:
[your improved version with specific metrics, action verbs, and impact]

Here is the resume to analyze:

{resume_text}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert resume reviewer. Always respond with the exact section headers requested. Never skip any section."
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
        return f"❌ Groq API error: {str(e)}"