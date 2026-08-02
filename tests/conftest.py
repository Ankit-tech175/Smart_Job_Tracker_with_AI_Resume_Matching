"""
Shared pytest fixtures for the test suite.

Sets required env vars BEFORE importing the app, so the app
factory picks up an isolated in-memory SQLite database instead
of touching the real dev database (instance/database.db).
"""

import os

# These must be set before `backend`/`config` are imported anywhere,
# since Config reads them at import time via os.getenv().
os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("JWT_SECRET_KEY", "test-jwt-secret-key")
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

import pytest

from backend import create_app
from backend.database.extensions import db


@pytest.fixture()
def app():
    """Create a fresh Flask app + in-memory DB schema for each test."""

    flask_app = create_app()
    flask_app.config.update(TESTING=True)

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    """A Flask test client bound to the app fixture above."""
    return app.test_client()


@pytest.fixture()
def registered_user(client):
    """Registers a user and returns their credentials."""

    payload = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "StrongPass123"
    }

    client.post("/api/auth/register", json=payload)

    return payload


@pytest.fixture()
def auth_headers(client, registered_user):
    """Registers + logs in a user, returns a ready-to-use auth header dict."""

    response = client.post(
        "/api/auth/login",
        json={
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
    )

    token = response.get_json()["data"]["access_token"]

    return {"Authorization": f"Bearer {token}"}
