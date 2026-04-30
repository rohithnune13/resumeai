# app.py — Full professional redesign
# CHUNK 1: imports, page config, CSS, navbar, hero

import streamlit as st
from extractor import extract_resume_text
from ai_feedback import get_resume_feedback
from utils import (
    parse_feedback_sections,
    parse_before_after,
    extract_score_number,
    get_score_color,
    get_score_label,
    extract_keywords_list
)

st.set_page_config(
    page_title="ResumeAI - Free Resume Feedback",
    page_icon="📄",
    layout="wide"
)

st.markdown("""
<style>
.block-container { padding-top: 0rem !important; }
header[data-testid="stHeader"] { display: none; }
.navbar {
    display: flex; align-items: center;
    justify-content: space-between;
    padding: 14px 40px;
    border-bottom: 1px solid #e5e7eb;
    background: white;
}
.nav-logo { display: flex; align-items: center; gap: 10px; }
.nav-logo-box {
    width: 30px; height: 30px; background: #1a56db;
    border-radius: 7px; display: flex; align-items: center;
    justify-content: center; color: white;
    font-weight: 700; font-size: 14px;
}
.nav-logo-text { font-size: 16px; font-weight: 600; color: #111; }
.nav-badge {
    font-size: 11px; background: #eff6ff; color: #1a56db;
    padding: 3px 9px; border-radius: 20px; font-weight: 500;
}
.hero {
    text-align: center; padding: 64px 20px 48px;
    background: white;
}
.hero-pill {
    display: inline-block; background: #eff6ff; color: #1a56db;
    font-size: 12px; font-weight: 500;
    padding: 5px 14px; border-radius: 20px; margin-bottom: 20px;
}
.hero h1 {
    font-size: 42px; font-weight: 700; color: #111;
    line-height: 1.2; margin-bottom: 16px;
}
.hero h1 span { color: #1a56db; }
.hero p {
    font-size: 17px; color: #6b7280;
    max-width: 480px; margin: 0 auto 28px; line-height: 1.6;
}
.hero-sub { font-size: 13px; color: #9ca3af; margin-top: 12px; }
.stats-bar {
    display: flex;
    border-top: 1px solid #e5e7eb;
    border-bottom: 1px solid #e5e7eb;
    background: white;
}
.stat-item {
    flex: 1; text-align: center; padding: 20px;
    border-right: 1px solid #e5e7eb;
}
.stat-item:last-child { border-right: none; }
.stat-num { font-size: 24px; font-weight: 700; color: #1a56db; }
.stat-label { font-size: 12px; color: #6b7280; margin-top: 3px; }
.features-row {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 16px; padding: 36px 40px; background: #f9fafb;
}
.feature-card {
    background: white; border: 1px solid #e5e7eb;
    border-radius: 12px; padding: 20px;
}
.feature-icon {
    width: 36px; height: 36px; border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; margin-bottom: 12px;
}
.feature-title { font-size: 14px; font-weight: 600; color: #111; margin-bottom: 5px; }
.feature-desc { font-size: 13px; color: #6b7280; line-height: 1.5; }
.fb-card {
    background: white; border: 1px solid #e5e7eb;
    border-radius: 12px; padding: 20px 24px;
    margin-bottom: 14px; border-left: 5px solid #ccc;
}
.fb-card.green  { border-left-color: #16a34a; }
.fb-card.orange { border-left-color: #d97706; }
.fb-card.blue   { border-left-color: #2563eb; }
.fb-card.purple { border-left-color: #7c3aed; }
.fb-title { font-size: 15px; font-weight: 600; color: #111; margin-bottom: 10px; }
.fb-content { font-size: 14px; color: #374151; line-height: 1.8; }
.score-card {
    background: #f9fafb; border: 1px solid #e5e7eb;
    border-radius: 14px; padding: 24px;
    display: flex; gap: 24px; align-items: center;
    margin-bottom: 20px;
}
.score-number { font-size: 52px; font-weight: 800; line-height: 1; }
.score-outof { font-size: 16px; color: #9ca3af; margin-top: 4px; }
.score-label { font-size: 18px; font-weight: 600; margin-top: 6px; }
.score-desc { font-size: 14px; color: #6b7280; margin-top: 4px; line-height: 1.5; }
.ba-grid {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 16px; margin-bottom: 20px;
}
.ba-card { border-radius: 12px; padding: 20px; border: 1px solid #e5e7eb; }
.ba-before { background: #f9fafb; }
.ba-after  { background: #eff6ff; border-color: #bfdbfe; }
.ba-label {
    font-size: 11px; font-weight: 700;
    letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 10px;
}
.ba-before .ba-label { color: #9ca3af; }
.ba-after  .ba-label { color: #1a56db; }
.ba-text { font-size: 14px; line-height: 1.7; color: #374151; }
.ba-after .ba-text { color: #1e40af; }
.keyword-pills { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 8px; }
.kw-pill {
    background: #eff6ff; color: #1a56db; font-size: 13px;
    font-weight: 500; padding: 6px 14px; border-radius: 20px;
    border: 1px solid #bfdbfe;
}
.footer {
    text-align: center; padding: 28px; font-size: 13px;
    color: #9ca3af; border-top: 1px solid #e5e7eb;
    background: #f9fafb; margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="navbar">
    <div class="nav-logo">
        <div class="nav-logo-box">R</div>
        <span class="nav-logo-text">ResumeAI</span>
        <span class="nav-badge">Free</span>
    </div>
    <div style="display:flex; gap:28px; align-items:center;">
        <span style="font-size:14px; color:#6b7280;">How it works</span>
        <span style="font-size:14px; color:#6b7280;">Examples</span>
    </div>
</div>
<div class="hero">
    <div class="hero-pill">AI-powered &nbsp;&#183;&nbsp; Free &nbsp;&#183;&nbsp; Instant</div>
    <h1>Get your resume scored by<br><span>expert AI</span> in seconds</h1>
    <p>Upload your resume and receive detailed, structured feedback
    on strengths, gaps, ATS compatibility, and more.</p>
    <div class="hero-sub">No signup required &nbsp;&#183;&nbsp; PDF or TXT
    &nbsp;&#183;&nbsp; Results in under 15 seconds</div>
</div>
<div class="stats-bar">
    <div class="stat-item">
        <div class="stat-num">10k+</div>
        <div class="stat-label">Resumes analysed</div>
    </div>
    <div class="stat-item">
        <div class="stat-num">4.9/5</div>
        <div class="stat-label">User satisfaction</div>
    </div>
    <div class="stat-item">
        <div class="stat-num">100%</div>
        <div class="stat-label">Free forever</div>
    </div>
</div>
<div class="features-row">
    <div class="feature-card">
        <div class="feature-icon" style="background:#eff6ff;">&#9889;</div>
        <div class="feature-title">Instant analysis</div>
        <div class="feature-desc">Structured AI feedback in under 15 seconds</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon" style="background:#f0fdf4;">&#10003;</div>
        <div class="feature-title">ATS optimisation</div>
        <div class="feature-desc">Know exactly which keywords you are missing</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon" style="background:#f5f3ff;">&#8635;</div>
        <div class="feature-title">Before vs after</div>
        <div class="feature-desc">AI rewrites your weakest bullet point for you</div>
    </div>
</div>
""", unsafe_allow_html=True)


# CHUNK 2: upload section, validation, analyse button

st.markdown("""
<div style="padding: 36px 40px 0px 40px; background: white;
border-top: 1px solid #e5e7eb;">
    <div style="font-size:22px; font-weight:600; color:#111;
    margin-bottom:6px;">Analyse your resume</div>
    <div style="font-size:14px; color:#6b7280;
    margin-bottom:24px;">Upload a PDF or TXT file to get started</div>
</div>
""", unsafe_allow_html=True)

col_l, col_m, col_r = st.columns([1, 2, 1])

with col_m:
    uploaded_file = st.file_uploader(
        label="Upload your resume",
        type=["pdf", "txt"],
        help="PDF or TXT - Max 200MB - Your data is never stored",
        label_visibility="collapsed"
    )


def validate_resume_text(text: str):
    if not text or len(text.strip()) == 0:
        return False, "No text found. The PDF may be image-based or scanned."
    if len(text.strip()) < 100:
        return False, "Text too short. Please upload a complete resume."
    return True, ""


if uploaded_file is not None:

    with col_m:
        st.success("✅ " + uploaded_file.name + " uploaded successfully")

    resume_text = extract_resume_text(uploaded_file)
    is_valid, error_msg = validate_resume_text(resume_text)

    if not is_valid:
        with col_m:
            st.error("❌ " + error_msg)
        st.stop()

    if len(resume_text) > 15000:
        resume_text = resume_text[:15000]

    with col_m:
        with st.expander("📃 View extracted text"):
            st.text_area(
                label="content",
                value=resume_text,
                height=250,
                disabled=True,
                label_visibility="collapsed"
            )
            st.caption(
                str(len(resume_text.split())) + " words - " +
                str(len(resume_text)) + " characters"
            )

        analyse_clicked = st.button(
            "🤖 Analyse My Resume",
            type="primary",
            use_container_width=True
        )

    if analyse_clicked:

        with col_m:
            progress = st.progress(0, text="Starting analysis...")
            progress.progress(30, text="📄 Reading resume...")
            progress.progress(60, text="🤖 Sending to AI...")
            feedback = get_resume_feedback(resume_text)
            progress.progress(90, text="📊 Building results...")

            if feedback.startswith("❌"):
                progress.empty()
                st.error(feedback)
                st.stop()

    from utils import calculate_resume_score
            sections = parse_feedback_sections(feedback)
            score_data = calculate_resume_score(resume_text)
            score_number = score_data["score"]
            score_color = get_score_color(score_number)
            score_label = get_score_label(score_number)
            before_text, after_text = parse_before_after(
                sections.get("beforeafter", "")
            )
            keywords = extract_keywords_list(sections.get("keywords", ""))
            progress.progress(100, text="✅ Done!")
            progress.empty()

        st.markdown("---")
        res_l, res_m, res_r = st.columns([0.5, 3, 0.5])

        with res_m:
            st.markdown(
                "<div style='font-size:20px; font-weight:700; color:#111;"
                "margin-bottom:4px;'>Your resume results</div>"
                "<div style='font-size:13px; color:#9ca3af;"
                "margin-bottom:24px;'>Powered by LLaMA 3.3 via Groq</div>",
                unsafe_allow_html=True
            )

            tab1, tab2, tab3, tab4 = st.tabs([
                "📊 Overview",
                "💬 Feedback",
                "🔄 Before vs After",
                "🔑 Keywords"
            ])

        # TAB 1: Overview
            with tab1:
                score_line = sections.get("score", "")[:200]

                st.markdown(
                    "<div class='score-card'>"
                    "<div>"
                    "<div class='score-number' style='color:" + score_color + ";'>" +
                    str(score_number) +
                    "</div>"
                    "<div class='score-outof'>out of 10</div>"
                    "</div>"
                    "<div style='flex:1;'>"
                    "<div class='score-label' style='color:" + score_color + ";'>" +
                    score_label +
                    "</div>"
                    "<div class='score-desc'>" + score_line + "</div>"
                    "</div>"
                    "</div>",
                    unsafe_allow_html=True
                )

                if score_number:
                    st.progress(score_number / 10)

                # Score breakdown table
                st.markdown(
                    "<div style='font-size:14px; font-weight:600; "
                    "margin: 16px 0 10px;'>Score breakdown</div>",
                    unsafe_allow_html=True
                )

                breakdown = score_data.get("breakdown", {})
                for signal, data in breakdown.items():
                    sig_score = data["score"]
                    sig_max = data["max"]
                    sig_detail = data["detail"]
                    sig_pct = sig_score / sig_max

                    if sig_pct >= 0.8:
                        sig_color = "#16a34a"
                    elif sig_pct >= 0.5:
                        sig_color = "#d97706"
                    else:
                        sig_color = "#dc2626"

                    st.markdown(
                        "<div style='display:flex; justify-content:space-between;"
                        "font-size:13px; margin-bottom:3px;'>"
                        "<span style='color:#374151;'>" + signal + "</span>"
                        "<span style='color:" + sig_color + "; font-weight:600;'>" +
                        str(sig_score) + " / " + str(sig_max) +
                        "</span></div>"
                        "<div style='font-size:11px; color:#9ca3af;"
                        "margin-bottom:8px;'>" + sig_detail + "</div>",
                        unsafe_allow_html=True
                    )
                    st.progress(sig_pct)

                # Top strength and priority cards
                c1, c2 = st.columns(2)

                strength_line = ""
                for line in sections.get("strengths", "").split("\n"):
                    cleaned = line.strip().lstrip("-• ")
                    if cleaned:
                        strength_line = cleaned
                        break

                improve_line = ""
                for line in sections.get("improvements", "").split("\n"):
                    cleaned = line.strip().lstrip("-• ")
                    if cleaned:
                        improve_line = cleaned
                        break

                with c1:
                    st.markdown(
                        "<div class='fb-card green'>"
                        "<div class='fb-title'>✅ Top Strength</div>"
                        "<div class='fb-content'>" + strength_line + "</div>"
                        "</div>",
                        unsafe_allow_html=True
                    )
                with c2:
                    st.markdown(
                        "<div class='fb-card orange'>"
                        "<div class='fb-title'>🔧 Top Priority</div>"
                        "<div class='fb-content'>" + improve_line + "</div>"
                        "</div>",
                        unsafe_allow_html=True
                    )
            # TAB 2: Full Feedback
            with tab2:
                st.markdown(
                    "<div class='fb-card green'>"
                    "<div class='fb-title'>✅ Strengths</div>"
                    "<div class='fb-content'>" +
                    sections.get("strengths", "") +
                    "</div></div>"
                    "<div class='fb-card orange'>"
                    "<div class='fb-title'>🔧 Areas for Improvement</div>"
                    "<div class='fb-content'>" +
                    sections.get("improvements", "") +
                    "</div></div>"
                    "<div class='fb-card purple'>"
                    "<div class='fb-title'>💡 ATS Suggestions</div>"
                    "<div class='fb-content'>" +
                    sections.get("ats", "") +
                    "</div></div>",
                    unsafe_allow_html=True
                )

            # TAB 3: Before vs After
            with tab3:
                st.markdown(
                    "<div style='font-size:14px; color:#6b7280;"
                    "margin-bottom:16px;'>AI identified your weakest bullet "
                    "point and rewrote it with stronger language and metrics."
                    "</div>",
                    unsafe_allow_html=True
                )

                if before_text and after_text:
                    st.markdown(
                        "<div class='ba-grid'>"
                        "<div class='ba-card ba-before'>"
                        "<div class='ba-label'>Before</div>"
                        "<div class='ba-text'>" + before_text + "</div>"
                        "</div>"
                        "<div class='ba-card ba-after'>"
                        "<div class='ba-label'>After</div>"
                        "<div class='ba-text'>" + after_text + "</div>"
                        "</div>"
                        "</div>",
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        "<div style='font-size:13px; color:#9ca3af;"
                        "margin-top:8px;'>💡 Use this rewrite as a template "
                        "for all your other bullet points.</div>",
                        unsafe_allow_html=True
                    )
                else:
                    st.info(
                        "Before/After could not be parsed. Try analysing again."
                    )

            # TAB 4: Keywords
            with tab4:
                st.markdown(
                    "<div style='font-size:14px; color:#6b7280;"
                    "margin-bottom:16px;'>Add these keywords to improve "
                    "ATS compatibility.</div>",
                    unsafe_allow_html=True
                )
                if keywords:
                    pills = "<div class='keyword-pills'>"
                    for kw in keywords:
                        pills += "<span class='kw-pill'>" + kw + "</span>"
                    pills += "</div>"
                    st.markdown(pills, unsafe_allow_html=True)
                else:
                    st.markdown(sections.get("keywords", "No keywords found."))

            # Download button
            st.markdown(
                "<div style='margin-top:24px;'></div>",
                unsafe_allow_html=True
            )

            download_content = (
                "RESUMEAI - FEEDBACK REPORT\n"
                "File: " + uploaded_file.name + "\n"
                "Score: " + str(score_number) + "/10 - " + score_label + "\n"
                + "=" * 50 + "\n\n"
                "STRENGTHS\n" + sections.get("strengths", "N/A") + "\n\n"
                "AREAS FOR IMPROVEMENT\n" +
                sections.get("improvements", "N/A") + "\n\n"
                "MISSING KEYWORDS\n" +
                sections.get("keywords", "N/A") + "\n\n"
                "ATS SUGGESTIONS\n" + sections.get("ats", "N/A") + "\n\n"
                "BEFORE AND AFTER\n"
                "Before: " + before_text + "\n"
                "After:  " + after_text + "\n\n"
                "OVERALL SCORE\n" + sections.get("score", "N/A")
            )

            st.download_button(
                label="💾 Download Full Report",
                data=download_content,
                file_name="resumeai_feedback.txt",
                mime="text/plain",
                use_container_width=True
            )

else:
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        c1, c2 = st.columns(2)
        with c1:
            st.success("✅ Strengths analysis")
            st.warning("🔧 Improvement areas")
        with c2:
            st.info("🔑 Missing keywords")
            st.error("🎯 Visual score")

st.markdown(
    "<div class='footer'>ResumeAI &nbsp;&#183;&nbsp; "
    "Built with Streamlit and Groq &nbsp;&#183;&nbsp; "
    "Free forever &nbsp;&#183;&nbsp; "
    "Your data is never stored</div>",
    unsafe_allow_html=True
)