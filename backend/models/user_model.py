from datetime import datetime

from backend.database.extensions import db


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(80),
        nullable=False,
        unique=True
    )

    email = db.Column(
        db.String(120),
        nullable=False,
        unique=True
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Relationship with Job Applications
    job_applications = db.relationship(
        "JobApplication",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    resume_analyses = db.relationship(
      "ResumeAnalysis",
       backref="user",
       lazy=True,
       cascade="all, delete-orphan"
   )
    def __repr__(self):

        return f"<User {self.username}>"