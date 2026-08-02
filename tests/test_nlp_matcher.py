"""
Unit tests for nlp/matcher.py — the ATS scoring engine.

These are pure-function tests: no Flask app, no database,
no file I/O. They exist so this exact class of bug can't
happen silently again:

    test_matcher.py used to call calculate_ats_score(resume_text,
    job_description) with raw strings after the function was
    refactored to expect skill lists — these tests would have
    caught that immediately.
"""

import pytest

from nlp.matcher import (
    calculate_ats_score,
    analyze_skill_gap,
    generate_resume_suggestions
)


def test_perfect_match_scores_high():

    resume_skills = ["python", "flask", "sql", "git"]
    job_skills = ["python", "flask", "sql", "git"]

    score = calculate_ats_score(resume_skills, job_skills)

    assert score > 90


def test_no_overlap_scores_low():

    resume_skills = ["photoshop", "illustrator"]
    job_skills = ["python", "flask", "sql"]

    score = calculate_ats_score(resume_skills, job_skills)

    assert score < 30


def test_partial_overlap_is_between_extremes():

    resume_skills = ["python", "sql"]
    job_skills = ["python", "flask", "sql", "docker"]

    score = calculate_ats_score(resume_skills, job_skills)

    assert 0 < score < 100


def test_empty_resume_skills_returns_zero():

    score = calculate_ats_score([], ["python", "flask"])
    assert score == 0


def test_empty_job_skills_returns_zero():

    score = calculate_ats_score(["python", "flask"], [])
    assert score == 0


def test_both_empty_returns_zero():

    assert calculate_ats_score([], []) == 0


def test_score_never_exceeds_100():

    resume_skills = ["python"] * 5
    job_skills = ["python"]

    score = calculate_ats_score(resume_skills, job_skills)

    assert score <= 100


def test_score_is_case_insensitive():

    score_lower = calculate_ats_score(["python", "flask"], ["python", "flask"])
    score_mixed = calculate_ats_score(["Python", "FLASK"], ["python", "flask"])

    assert score_lower == score_mixed


def test_analyze_skill_gap_matched_and_missing():

    resume_skills = ["python", "flask", "git"]
    job_skills = ["python", "flask", "docker", "aws"]

    result = analyze_skill_gap(resume_skills, job_skills)

    assert result["matched_skills"] == ["flask", "python"]
    assert result["missing_skills"] == ["aws", "docker"]


def test_analyze_skill_gap_no_missing_skills():

    resume_skills = ["python", "flask", "docker"]
    job_skills = ["python", "flask"]

    result = analyze_skill_gap(resume_skills, job_skills)

    assert result["missing_skills"] == []


def test_generate_suggestions_low_score_message():

    suggestions = generate_resume_suggestions([], ats_score=30)

    assert "low" in suggestions[0].lower()


def test_generate_suggestions_high_score_message():

    suggestions = generate_resume_suggestions([], ats_score=90)

    assert "strong" in suggestions[0].lower()


def test_generate_suggestions_known_skill_has_specific_advice():

    suggestions = generate_resume_suggestions(["docker"], ats_score=60)

    joined = " ".join(suggestions).lower()

    assert "docker" in joined


def test_generate_suggestions_unknown_skill_has_generic_advice():

    suggestions = generate_resume_suggestions(["kubernetes"], ats_score=60)

    joined = " ".join(suggestions).lower()

    assert "kubernetes" in joined
