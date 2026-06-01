import csv
import os

import spacy

from PyPDF2 import PdfReader


# Load spaCy model
nlp = spacy.load("en_core_web_sm")


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
                skills.append(
                    row[0].strip().lower()
                )

    return skills


# Load skills once
SKILLS_DB = load_skills()


# =========================
# EXTRACT TEXT FROM PDF
# =========================
def extract_text_from_pdf(pdf_path):

    text = ""

    reader = PdfReader(pdf_path)

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted + " "

    return text


# =========================
# EXTRACT SKILLS
# =========================
def extract_skills(text):

    doc = nlp(text.lower())

    extracted_skills = set()

    for token in doc:

        if token.text in SKILLS_DB:

            extracted_skills.add(
                token.text
            )

    return list(extracted_skills)


# =========================
# PARSE RESUME
# =========================
def parse_resume(pdf_path):

    # Extract raw text
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