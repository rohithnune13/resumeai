# extractor.py
# Uses pdfplumber instead of PyMuPDF — works on all Windows setups

import pdfplumber
import streamlit as st


def extract_text_from_pdf(uploaded_file) -> str:
    """
    Takes a Streamlit uploaded file object (PDF),
    extracts and returns all text as a single string.
    """
    try:
        all_text = ""

        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    all_text += page_text + "\n"

        return all_text.strip()

    except Exception as e:
        st.error(f"❌ Failed to read PDF: {e}")
        return ""


def extract_text_from_txt(uploaded_file) -> str:
    """
    Takes a Streamlit uploaded file object (TXT),
    reads and returns the text content.
    """
    try:
        text = uploaded_file.read().decode("utf-8", errors="ignore")
        return text.strip()

    except Exception as e:
        st.error(f"❌ Failed to read text file: {e}")
        return ""


def extract_resume_text(uploaded_file) -> str:
    """
    Master function — routes to the correct extractor
    based on file type.
    """
    if uploaded_file is None:
        return ""

    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)

    elif filename.endswith(".txt"):
        return extract_text_from_txt(uploaded_file)

    else:
        st.error("❌ Unsupported file type. Please upload a PDF or TXT file.")
        return ""