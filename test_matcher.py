from nlp.parser import parse_resume

from nlp.matcher import (
    calculate_ats_score,
    extract_job_skills
)


# =========================
# LOAD RESUME
# =========================

resume_path = "uploads/Ankit_Chauhan_Resume_v3.pdf"

parsed_resume = parse_resume(
    resume_path
)

resume_text = parsed_resume["resume_text"]


# =========================
# SAMPLE JOB DESCRIPTION
# =========================

job_description = """

We are hiring a Python Flask Developer.

Required Skills:

- Python
- Flask
- REST API
- SQL
- Git
- Machine Learning
- scikit-learn

Experience with NLP is a plus.

"""


# =========================
# EXTRACT JD SKILLS
# =========================

job_skills = extract_job_skills(
    job_description
)


# =========================
# CALCULATE ATS SCORE
# =========================

ats_score = calculate_ats_score(
    resume_text,
    job_description
)


# =========================
# PRINT RESULTS
# =========================

print("\n===== ATS MATCH RESULT =====\n")

print("Job Skills:\n")

print(job_skills)

print("\nATS Match Score:\n")

print(f"{ats_score}%")

print("\n============================\n")