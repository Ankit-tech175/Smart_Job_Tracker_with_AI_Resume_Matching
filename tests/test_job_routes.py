"""
Tests for /api/jobs/* — CRUD, analytics, ownership isolation,
and CSV export.
"""

import io


def _add_job(client, auth_headers, **overrides):

    payload = {
        "company_name": "Acme Corp",
        "job_title": "Backend Engineer",
        "job_link": "https://acme.example.com/careers/1",
        "status": "Applied",
        "notes": "Referred by a friend"
    }

    payload.update(overrides)

    return client.post(
        "/api/jobs/add",
        json=payload,
        headers=auth_headers
    )


def test_add_job_requires_auth(client):

    response = client.post(
        "/api/jobs/add",
        json={"company_name": "Acme", "job_title": "Engineer"}
    )

    # No Authorization header → JWT rejects the request
    assert response.status_code == 401


def test_add_job_success(client, auth_headers):

    response = _add_job(client, auth_headers)
    body = response.get_json()

    assert response.status_code == 201
    assert body["success"] is True
    assert body["data"]["company_name"] == "Acme Corp"


def test_add_job_missing_required_fields(client, auth_headers):

    response = client.post(
        "/api/jobs/add",
        json={"company_name": "Acme Corp"},
        headers=auth_headers
    )

    assert response.status_code == 400


def test_default_status_is_applied(client, auth_headers):

    response = _add_job(client, auth_headers, status="")
    body = response.get_json()

    assert body["data"]["status"] == "Applied"


def test_get_user_jobs(client, auth_headers):

    _add_job(client, auth_headers)
    _add_job(client, auth_headers, company_name="Globex")

    response = client.get(
        "/api/jobs/my-jobs",
        headers=auth_headers
    )

    body = response.get_json()

    assert response.status_code == 200
    assert len(body["data"]) == 2


def test_update_job_status(client, auth_headers):

    add_response = _add_job(client, auth_headers)
    job_id = add_response.get_json()["data"]["job_id"]

    response = client.put(
        f"/api/jobs/update-status/{job_id}",
        json={"status": "Interview"},
        headers=auth_headers
    )

    body = response.get_json()

    assert response.status_code == 200
    assert body["data"]["updated_status"] == "Interview"


def test_delete_job(client, auth_headers):

    add_response = _add_job(client, auth_headers)
    job_id = add_response.get_json()["data"]["job_id"]

    response = client.delete(
        f"/api/jobs/delete/{job_id}",
        headers=auth_headers
    )

    assert response.status_code == 200

    # Confirm it's really gone
    fetch_response = client.get(
        "/api/jobs/my-jobs",
        headers=auth_headers
    )
    assert fetch_response.get_json()["data"] == []


def test_user_cannot_update_another_users_job(client, auth_headers):
    """
    Ownership isolation check: a second user should not be able
    to modify the first user's job application.
    """

    add_response = _add_job(client, auth_headers)
    job_id = add_response.get_json()["data"]["job_id"]

    # Register + log in as a second, different user
    client.post(
        "/api/auth/register",
        json={
            "username": "second_user",
            "email": "second_user@example.com",
            "password": "AnotherPass123"
        }
    )

    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "second_user@example.com",
            "password": "AnotherPass123"
        }
    )

    second_user_token = login_response.get_json()["data"]["access_token"]
    second_user_headers = {
        "Authorization": f"Bearer {second_user_token}"
    }

    response = client.put(
        f"/api/jobs/update-status/{job_id}",
        json={"status": "Rejected"},
        headers=second_user_headers
    )

    # Job is scoped by user_id, so it "doesn't exist" for this user
    assert response.status_code == 404


def test_analytics_counts(client, auth_headers):

    _add_job(client, auth_headers, status="Applied")
    _add_job(client, auth_headers, status="Interview")
    _add_job(client, auth_headers, status="Offer")

    response = client.get(
        "/api/jobs/analytics",
        headers=auth_headers
    )

    body = response.get_json()["data"]

    assert body["total_applications"] == 3
    assert body["applied_count"] == 1
    assert body["interview_count"] == 1
    assert body["offer_count"] == 1
    assert body["rejected_count"] == 0


def test_export_csv_returns_csv_file(client, auth_headers):

    _add_job(client, auth_headers, company_name="Acme Corp")

    response = client.get(
        "/api/jobs/export-csv",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.mimetype == "text/csv"
    assert "attachment" in response.headers["Content-Disposition"]

    csv_text = response.data.decode("utf-8")

    assert "Company Name" in csv_text  # header row present
    assert "Acme Corp" in csv_text     # our job row present


def test_export_csv_requires_auth(client):

    response = client.get("/api/jobs/export-csv")

    assert response.status_code == 401
