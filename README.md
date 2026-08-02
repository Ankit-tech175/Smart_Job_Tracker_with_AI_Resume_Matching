# Smart Job Tracker with AI Resume Matching

A full-stack job application tracker built with Flask, NLP, and Machine Learning — JWT auth, job pipeline tracking, and an AI resume-matching engine (spaCy + TF-IDF/cosine similarity) that scores a resume against a job description.

## Features

- JWT-based authentication (register/login)
- Job application CRUD with per-user data isolation
- Live analytics dashboard (Chart.js doughnut chart + progress bars)
- CSV export of your job applications
- AI resume analyzer: ATS match score, matched/missing skills, and improvement suggestions
- Alembic-managed database migrations
- `pytest` test suite (auth, job CRUD, ownership isolation, ATS scoring edge cases)

## Tech Stack

- **Backend:** Flask, Flask-SQLAlchemy, Flask-JWT-Extended, Flask-Migrate (Alembic)
- **NLP/ML:** spaCy, scikit-learn (TF-IDF + cosine similarity), PyPDF2
- **Frontend:** Bootstrap 5, Chart.js, vanilla JavaScript
- **Database:** SQLite (dev) / PostgreSQL (prod-ready via `DATABASE_URL`)

## Local Setup

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
python -m spacy download en_core_web_sm

cp .env.example .env         # then fill in real secret values

flask db upgrade
python app.py
```

## Running Tests

```bash
pip install -r requirements-dev.txt
pytest -v
```

## Docs

- `docs/architecture_diagram.svg` — system architecture
- `docs/er_diagram.svg` — entity relationship diagram

## Deployment

See the project's interview-prep/deployment notes for a step-by-step Render deployment guide (Procfile + gunicorn already included).
