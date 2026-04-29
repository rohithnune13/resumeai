# utils.py
# Parses all feedback sections including before/after and score

import re


def parse_feedback_sections(feedback_text: str) -> dict:
    """
    Splits AI feedback into individual sections.
    Returns a dictionary with one key per section.
    """
    sections = {
        "strengths":    "## ✅ Strengths",
        "improvements": "## 🔧 Areas for Improvement",
        "keywords":     "## 🔑 Missing Keywords",
        "ats":          "## 💡 ATS Suggestions",
        "score":        "## 🎯 Overall Score",
        "beforeafter":  "## 🔄 Before & After"
    }

    result = {}
    headers = list(sections.values())

    for key, header in sections.items():
        start = feedback_text.find(header)
        if start == -1:
            result[key] = ""
            continue
        start = start + len(header)
        end = len(feedback_text)
        for other_header in headers:
            if other_header == header:
                continue
            next_start = feedback_text.find(other_header, start)
            if next_start != -1 and next_start < end:
                end = next_start
        result[key] = feedback_text[start:end].strip()

    return result


def parse_before_after(beforeafter_text: str) -> tuple[str, str]:
    """
    Extracts the BEFORE and AFTER text from the before/after section.
    Returns (before_text, after_text) as a tuple.
    """
    if not beforeafter_text:
        return "", ""

    before = ""
    after = ""

    # Find BEFORE block
    before_match = re.search(
        r'BEFORE:\s*\n(.*?)(?=AFTER:|$)',
        beforeafter_text,
        re.DOTALL | re.IGNORECASE
    )
    if before_match:
        before = before_match.group(1).strip()
        # Remove surrounding brackets if AI added them
        before = before.strip("[]").strip()

    # Find AFTER block
    after_match = re.search(
        r'AFTER:\s*\n(.*?)$',
        beforeafter_text,
        re.DOTALL | re.IGNORECASE
    )
    if after_match:
        after = after_match.group(1).strip()
        after = after.strip("[]").strip()

    return before, after


def extract_score_number(score_text: str) -> float:
    """
    Pulls the numeric score out of the score section.
    Handles: 7.5/10, 8/10, 7.5 out of 10
    """
    if not score_text:
        return None

    patterns = [
        r'(\d+\.?\d*)\s*/\s*10',
        r'(\d+\.?\d*)\s+out\s+of\s+10'
    ]
    for pattern in patterns:
        match = re.search(pattern, score_text, re.IGNORECASE)
        if match:
            score = float(match.group(1))
            return max(0.0, min(10.0, score))
    return None


def get_score_color(score: float) -> str:
    if score is None:
        return "#888888"
    if score >= 8.0:
        return "#3B6D11"
    elif score >= 6.0:
        return "#BA7517"
    else:
        return "#A32D2D"


def get_score_label(score: float) -> str:
    if score is None:
        return "Not rated"
    if score >= 8.5:
        return "Excellent"
    elif score >= 7.0:
        return "Strong"
    elif score >= 5.5:
        return "Average"
    else:
        return "Needs work"


def extract_keywords_list(keywords_text: str) -> list[str]:
    """
    Converts the keywords section text into a clean list of strings.
    """
    if not keywords_text:
        return []

    keywords = []
    for line in keywords_text.split("\n"):
        line = line.strip()
        # Remove bullet characters
        line = re.sub(r'^[-•*]\s*', '', line)
        if line:
            keywords.append(line)
    return keywords