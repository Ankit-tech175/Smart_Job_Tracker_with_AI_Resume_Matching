"""
Tests for /api/auth/* — register, login, and validation edge cases.
"""


def test_register_success(client):

    response = client.post(
        "/api/auth/register",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "password123"
        }
    )

    body = response.get_json()

    assert response.status_code == 201
    assert body["success"] is True


def test_register_missing_fields(client):

    response = client.post(
        "/api/auth/register",
        json={"username": "alice"}
    )

    body = response.get_json()

    assert response.status_code == 400
    assert body["success"] is False


def test_register_duplicate_username(client, registered_user):

    response = client.post(
        "/api/auth/register",
        json={
            "username": registered_user["username"],
            "email": "different_email@example.com",
            "password": "password123"
        }
    )

    body = response.get_json()

    assert response.status_code == 409
    assert body["success"] is False


def test_register_duplicate_email(client, registered_user):

    response = client.post(
        "/api/auth/register",
        json={
            "username": "a_different_username",
            "email": registered_user["email"],
            "password": "password123"
        }
    )

    body = response.get_json()

    assert response.status_code == 409
    assert body["success"] is False


def test_login_success(client, registered_user):

    response = client.post(
        "/api/auth/login",
        json={
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
    )

    body = response.get_json()

    assert response.status_code == 200
    assert body["success"] is True
    assert "access_token" in body["data"]


def test_login_wrong_password(client, registered_user):

    response = client.post(
        "/api/auth/login",
        json={
            "email": registered_user["email"],
            "password": "totally-wrong-password"
        }
    )

    body = response.get_json()

    assert response.status_code == 401
    assert body["success"] is False


def test_login_nonexistent_user(client):

    response = client.post(
        "/api/auth/login",
        json={
            "email": "nobody@example.com",
            "password": "whatever123"
        }
    )

    assert response.status_code == 401


def test_password_is_never_stored_in_plaintext(client, registered_user):
    """
    Confirms passwords are hashed at rest, not stored raw
    — an important thing to be able to demonstrate live.
    """

    from backend.models.user_model import User

    user = User.query.filter_by(
        email=registered_user["email"]
    ).first()

    assert user.password != registered_user["password"]
    assert user.password.startswith("pbkdf2:") or ":" in user.password
