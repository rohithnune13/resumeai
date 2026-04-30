# utils.py

import re


def parse_feedback_sections(feedback_text: str) -> dict:
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


def parse_before_after(beforeafter_text: str):
    if not beforeafter_text:
        return "", ""
    before = ""
    after = ""
    before_match = re.search(
        r'BEFORE:\s*\n(.*?)(?=AFTER:|$)',
        beforeafter_text,
        re.DOTALL | re.IGNORECASE
    )
    if before_match:
        before = before_match.group(1).strip().strip("[]").strip()
    after_match = re.search(
        r'AFTER:\s*\n(.*?)$',
        beforeafter_text,
        re.DOTALL | re.IGNORECASE
    )
    if after_match:
        after = after_match.group(1).strip().strip("[]").strip()
    return before, after


def extract_score_number(score_text: str):
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


def extract_keywords_list(keywords_text: str) -> list:
    if not keywords_text:
        return []
    keywords = []
    for line in keywords_text.split("\n"):
        line = line.strip()
        line = re.sub(r'^[-*]\s*', '', line)
        if line:
            keywords.append(line)
    return keywords


def calculate_resume_score(resume_text: str) -> dict:
    text_lower = resume_text.lower()
    words = resume_text.split()
    word_count = len(words)
    breakdown = {}

    # 1. Quantified Achievements (2.0 pts)
    number_patterns = [
        r'\d+%',
        r'\$[\d,]+',
        r'\d+\+',
        r'\b\d{2,}\b',
        r'increased|decreased|reduced|improved|grew|saved|generated',
    ]
    metric_count = 0
    for pattern in number_patterns:
        metric_count += len(re.findall(pattern, resume_text, re.IGNORECASE))

    if metric_count >= 10:
        quant_score = 2.0
        quant_detail = "Strong use of metrics and numbers"
    elif metric_count >= 5:
        quant_score = 1.3
        quant_detail = "Some metrics present but could add more"
    elif metric_count >= 2:
        quant_score = 0.7
        quant_detail = "Very few quantified achievements"
    else:
        quant_score = 0.2
        quant_detail = "No quantified achievements found"

    breakdown["Quantified achievements"] = {
        "score": quant_score, "max": 2.0, "detail": quant_detail
    }

    # 2. Action Verbs (1.5 pts)
    action_verbs = [
        "developed", "built", "designed", "implemented", "created",
        "managed", "led", "optimized", "automated", "delivered",
        "improved", "increased", "reduced", "launched", "collaborated",
        "architected", "deployed", "integrated", "maintained", "tested",
        "analyzed", "executed", "coordinated", "established", "drove"
    ]
    verb_count = sum(1 for verb in action_verbs if verb in text_lower)

    if verb_count >= 10:
        verb_score = 1.5
        verb_detail = "Excellent use of action verbs"
    elif verb_count >= 6:
        verb_score = 1.0
        verb_detail = "Good use of action verbs"
    elif verb_count >= 3:
        verb_score = 0.5
        verb_detail = "Some action verbs but needs more"
    else:
        verb_score = 0.1
        verb_detail = "Very few action verbs found"

    breakdown["Action verbs"] = {
        "score": verb_score, "max": 1.5, "detail": verb_detail
    }

    # 3. Resume Sections (1.5 pts)
    expected_sections = [
        ["experience", "work experience", "employment"],
        ["education", "academic"],
        ["skills", "technical skills"],
        ["summary", "objective", "profile"],
        ["projects", "certifications", "achievements"]
    ]
    sections_found = 0
    for section_group in expected_sections:
        if any(s in text_lower for s in section_group):
            sections_found += 1

    section_score = round((sections_found / len(expected_sections)) * 1.5, 2)
    breakdown["Resume sections"] = {
        "score": section_score,
        "max": 1.5,
        "detail": str(sections_found) + " of 5 expected sections found"
    }

    # 4. Length (1.0 pt)
    if 400 <= word_count <= 800:
        length_score = 1.0
        length_detail = "Ideal length (" + str(word_count) + " words)"
    elif 300 <= word_count < 400 or 800 < word_count <= 1000:
        length_score = 0.6
        length_detail = "Acceptable length (" + str(word_count) + " words)"
    elif word_count > 1000:
        length_score = 0.3
        length_detail = "Too long (" + str(word_count) + " words) - aim for 400-800"
    else:
        length_score = 0.2
        length_detail = "Too short (" + str(word_count) + " words) - add more detail"

    breakdown["Resume length"] = {
        "score": length_score, "max": 1.0, "detail": length_detail
    }

    # 5. Keyword Density (2.0 pts)
    tech_keywords = [
        "python", "java", "javascript", "sql", "aws", "azure", "docker",
        "kubernetes", "react", "node", "git", "api", "agile", "scrum",
        "ci/cd", "jenkins", "selenium", "pytest", "swift", "kotlin",
        "machine learning", "data", "cloud", "devops", "testing",
        "automation", "rest", "microservices", "linux", "typescript"
    ]
    keyword_count = sum(1 for kw in tech_keywords if kw in text_lower)

    if keyword_count >= 15:
        kw_score = 2.0
        kw_detail = "Excellent keyword coverage (" + str(keyword_count) + " keywords)"
    elif keyword_count >= 10:
        kw_score = 1.5
        kw_detail = "Good keyword coverage (" + str(keyword_count) + " keywords)"
    elif keyword_count >= 5:
        kw_score = 1.0
        kw_detail = "Average keyword coverage (" + str(keyword_count) + " keywords)"
    else:
        kw_score = 0.3
        kw_detail = "Poor keyword coverage (" + str(keyword_count) + " keywords)"

    breakdown["Keyword density"] = {
        "score": kw_score, "max": 2.0, "detail": kw_detail
    }

    # 6. Summary Quality (1.0 pt)
    has_summary = any(
        s in text_lower for s in ["summary", "objective", "profile", "about"]
    )
    generic_words = [
        "experienced", "motivated", "skilled", "passionate",
        "proven", "dedicated", "results", "years of experience"
    ]
    generic_count = sum(1 for w in generic_words if w in text_lower)

    if has_summary and generic_count <= 2:
        summary_score = 1.0
        summary_detail = "Strong specific summary"
    elif has_summary and generic_count <= 4:
        summary_score = 0.6
        summary_detail = "Summary present but somewhat generic"
    elif has_summary:
        summary_score = 0.3
        summary_detail = "Summary too generic - make it specific"
    else:
        summary_score = 0.0
        summary_detail = "No summary section found"

    breakdown["Summary quality"] = {
        "score": summary_score, "max": 1.0, "detail": summary_detail
    }

    # 7. Contact Information (1.0 pt)
    has_email = bool(re.search(r'[\w.-]+@[\w.-]+\.\w+', resume_text))
    has_phone = bool(re.search(r'[\+\(]?[\d\s\-\(\)]{7,15}', resume_text))
    has_linkedin = "linkedin" in text_lower
    has_github = "github" in text_lower
    contact_count = sum([has_email, has_phone, has_linkedin, has_github])

    if contact_count >= 3:
        contact_score = 1.0
        contact_detail = "Complete contact information"
    elif contact_count == 2:
        contact_score = 0.6
        contact_detail = "Basic contact info - add LinkedIn or GitHub"
    else:
        contact_score = 0.2
        contact_detail = "Missing important contact information"

    breakdown["Contact information"] = {
        "score": contact_score, "max": 1.0, "detail": contact_detail
    }

    # Final Score
    total = round(
        quant_score + verb_score + section_score +
        length_score + kw_score + summary_score + contact_score,
        1
    )
    total = max(1.0, min(10.0, total))

    return {
        "score": total,
        "breakdown": breakdown,
        "word_count": word_count,
        "metric_count": metric_count,
        "verb_count": verb_count,
        "keyword_count": keyword_count
    }