import csv
import os
import re

import spacy

from PyPDF2 import PdfReader


# =========================
# LOAD SPACY MODEL
# =========================

nlp = spacy.load(
    "en_core_web_sm"
)


# =========================
# LOAD SKILLS DATASET
# =========================

def load_skills():

    skills_path = os.path.join(
        os.path.dirname(__file__),
        "skills.csv"
    )

    skills = []

    with open(
        skills_path,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.reader(file)

        for row in reader:

            if row:

                skill = row[0].strip().lower()

                if skill:

                    skills.append(skill)

    return sorted(
        list(set(skills))
    )


# Load skills globally
SKILLS_DB = load_skills()


# =========================
# EXTRACT TEXT FROM PDF
# =========================

def extract_text_from_pdf(pdf_path):

    text = ""

    try:

        reader = PdfReader(pdf_path)

        for page in reader.pages:

            extracted = page.extract_text()

            if extracted:

                text += extracted + " "

    except Exception as e:

        print(f"PDF Extraction Error: {e}")

    return text


# =========================
# CLEAN TEXT
# =========================

def clean_text(text):

    if not text:

        return ""

    return str(text).lower().strip()


# =========================
# EXTRACT SKILLS
# =========================

def extract_skills(text):

    """
    Advanced skill extraction:
    - Single-word skills
    - Multi-word skills
    - Exact regex matching
    """

    text = clean_text(text)

    # Prevent empty processing
    if not text:

        return []

    extracted_skills = set()

    # NLP processing
    doc = nlp(text)

    # Extract tokens
    tokens = set(

        token.text.lower()

        for token in doc

        if not token.is_stop
        and not token.is_punct
    )

    # Skill matching
    for skill in SKILLS_DB or []:

        try:

            # Exact regex boundary matching
            pattern = rf"\b{re.escape(skill.lower())}\b"

            # Multi-word skills
            if " " in skill:

                if re.search(pattern, text):

                    extracted_skills.add(skill)

            # Single-word skills
            else:

                if skill.lower() in tokens:

                    extracted_skills.add(skill)

        except re.error:

            continue

    return sorted(
        list(extracted_skills)
    )


# =========================
# PARSE RESUME
# =========================

def parse_resume(pdf_path):

    # Extract resume text
    resume_text = extract_text_from_pdf(
        pdf_path
    )

    # Extract skills
    skills = extract_skills(
        resume_text
    )

    return {

        "resume_text": resume_text,

        "skills": skills
    }