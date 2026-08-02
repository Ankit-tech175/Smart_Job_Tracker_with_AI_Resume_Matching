from datetime import datetime

from backend.database.extensions import db


class ResumeAnalysis(db.Model):

    __tablename__ = "resume_analyses"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    ats_score = db.Column(
        db.Float,
        nullable=False
    )

    matched_skills = db.Column(
        db.Text,
        nullable=True
    )

    missing_skills = db.Column(
        db.Text,
        nullable=True
    )

    recommendations = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Relationship
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    def __repr__(self):

        return f"<ResumeAnalysis {self.id}>"