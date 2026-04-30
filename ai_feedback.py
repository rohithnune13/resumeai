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
You are a brutally honest resume reviewer and senior tech recruiter.
You have high standards and you do NOT give inflated scores.

SCORING RULES — follow these strictly:
- 9.0 to 10.0 = Near perfect. Rare. Only for exceptional resumes with strong metrics, clean formatting, relevant keywords, and clear impact.
- 7.0 to 8.9 = Good resume but has clear gaps. Most resumes fall here.
- 5.0 to 6.9 = Average. Missing metrics, weak summary, or poor ATS optimization.
- 3.0 to 4.9 = Below average. Major issues with structure, relevance, or clarity.
- 1.0 to 2.9 = Poor. Needs complete rewrite.

You MUST vary your score based on the actual quality of THIS specific resume.
Do NOT default to 8.5. Evaluate honestly and critically.

Analyze the resume below and respond EXACTLY using these section headers:

## ✅ Strengths
- List exactly 4 specific strengths from THIS resume
- Reference actual content, job titles, tools, or projects mentioned

## 🔧 Areas for Improvement
- List exactly 4 concrete improvements needed
- Be direct, critical, and specific to THIS resume

## 🔑 Missing Keywords
- List exactly 6 keywords missing from THIS resume
- Focus on ATS keywords relevant to the candidate's target role

## 💡 ATS Suggestions
- List exactly 4 specific ATS formatting fixes for THIS resume

## 🎯 Overall Score
Score: X.X/10
One honest sentence explaining exactly why this score was given.

## 🔄 Before & After
Find the single weakest bullet point in the work experience section.
Rewrite it with strong action verbs, specific metrics, and clear impact.

BEFORE:
[copy the exact weak bullet point here]

AFTER:
[rewritten version with metrics and impact]

Here is the resume to analyze:

{resume_text}
"""

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