from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import cosine_similarity

from nlp.parser import extract_skills


# =========================
# PREPROCESS TEXT
# =========================
def preprocess_text(text):

    return text.lower().strip()


# =========================
# EXTRACT JOB DESCRIPTION SKILLS
# =========================
def extract_job_skills(job_description):

    return extract_skills(job_description)


# =========================
# CALCULATE ATS SCORE
# =========================
def calculate_ats_score(
    resume_text,
    job_description
):

    # Preprocess text
    resume_text = preprocess_text(
        resume_text
    )

    job_description = preprocess_text(
        job_description
    )

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform([
        resume_text,
        job_description
    ])

    # Calculate cosine similarity
    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    # Convert to percentage
    ats_score = round(
        similarity * 100,
        2
    )

    return ats_score