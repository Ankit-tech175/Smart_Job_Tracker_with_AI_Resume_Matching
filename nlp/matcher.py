from sklearn.feature_extraction.text import (
    TfidfVectorizer
)

from sklearn.metrics.pairwise import (
    cosine_similarity
)

from nlp.parser import extract_skills


# =========================
# PREPROCESS TEXT
# =========================
def preprocess_text(text):

    return text.lower().strip()


# =========================
# EXTRACT JOB DESCRIPTION SKILLS
# =========================
def extract_job_skills(
    job_description
):

    return extract_skills(
        job_description
    )


# =========================
# CALCULATE ATS SCORE
# =========================
def calculate_ats_score(
    resume_skills,
    job_skills
):

    """
    Calculate ATS score using
    extracted skills instead
    of full resume text.
    """

    # Clean skills
    resume_skills = [

        preprocess_text(skill)

        for skill in resume_skills

        if skill.strip()
    ]

    job_skills = [

        preprocess_text(skill)

        for skill in job_skills

        if skill.strip()
    ]

    # Prevent empty input
    if not resume_skills or not job_skills:

        return 0

    # Convert to text
    resume_text = " ".join(
        resume_skills
    )

    job_text = " ".join(
        job_skills
    )

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform([

        resume_text,
        job_text
    ])

    # Cosine Similarity
    similarity = cosine_similarity(

        vectors[0:1],
        vectors[1:2]

    )[0][0]

    # Skill overlap bonus
    matched_skills = set(
        resume_skills
    ).intersection(
        set(job_skills)
    )

    overlap_ratio = len(
        matched_skills
    ) / len(
        set(job_skills)
    )

    # Hybrid ATS calculation
    ats_score = (

        (similarity * 0.7) +

        (overlap_ratio * 0.3)

    ) * 100

    # Limit score
    ats_score = min(
        round(ats_score, 2),
        100
    )

    return ats_score


# =========================
# ANALYZE SKILL GAP
# =========================
def analyze_skill_gap(
    resume_skills,
    job_skills
):

    # Clean skill sets
    resume_set = set(

        skill.lower().strip()

        for skill in resume_skills

        if skill.strip()
    )

    job_set = set(

        skill.lower().strip()

        for skill in job_skills

        if skill.strip()
    )

    # Find matched skills
    matched_skills = sorted(

        list(
            resume_set.intersection(
                job_set
            )
        )
    )

    # Find missing skills
    missing_skills = sorted(

        list(
            job_set.difference(
                resume_set
            )
        )
    )

    return {

        "matched_skills":
            matched_skills,

        "missing_skills":
            missing_skills
    }


# =========================
# GENERATE AI SUGGESTIONS
# =========================
def generate_resume_suggestions(
    missing_skills,
    ats_score
):

    """
    Generate intelligent
    resume improvement
    suggestions.
    """

    suggestions = []

    # ATS-based suggestions
    if ats_score < 50:

        suggestions.append(
            "Your ATS score is low. Add more relevant technical skills and projects related to the job description."
        )

    elif ats_score < 75:

        suggestions.append(
            "Your resume partially matches the job description. Improve keyword alignment and project descriptions."
        )

    else:

        suggestions.append(
            "Your resume has a strong ATS match. Focus on improving project impact and measurable achievements."
        )

    # Skill-based suggestions
    for skill in missing_skills:

        if skill == "docker":

            suggestions.append(
                "Add Docker-based deployment or containerization projects to strengthen backend and DevOps profile."
            )

        elif skill == "aws":

            suggestions.append(
                "Include cloud deployment experience using AWS services such as EC2, S3, or Lambda."
            )

        elif skill == "postgresql":

            suggestions.append(
                "Mention PostgreSQL database design, queries, or backend integration projects."
            )

        elif skill == "flask":

            suggestions.append(
                "Add Flask REST API projects to improve backend development alignment."
            )

        elif skill == "machine learning":

            suggestions.append(
                "Include machine learning projects with model training, evaluation, and deployment experience."
            )

        elif skill == "react":

            suggestions.append(
                "Add responsive frontend projects using React and component-based architecture."
            )

        else:

            suggestions.append(
                f"Consider adding hands-on experience or projects related to {skill}."
            )

    return suggestions