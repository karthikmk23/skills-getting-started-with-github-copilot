import os
import sys

from fastapi.testclient import TestClient

# Ensure src is importable
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from app import app

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister():
    activity = "Chess Club"
    email = "pytest_user@example.com"

    # Ensure clean state for the test
    resp = client.get("/activities")
    participants = resp.json()[activity]["participants"]
    if email in participants:
        client.post(f"/activities/{activity}/unregister", params={"email": email})

    # Sign up
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]

    # Unregister
    resp = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert resp.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]
