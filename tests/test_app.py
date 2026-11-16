import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    snapshot = copy.deepcopy(activities)
    yield TestClient(app)
    activities.clear()
    activities.update(snapshot)


def test_signup_rejects_duplicate_email(client):
    email = "new@mergington.edu"
    first = client.post("/activities/Chess Club/signup", params={"email": email})
    second = client.post("/activities/Chess Club/signup", params={"email": email})

    assert first.status_code == 200
    assert second.status_code == 400
    assert activities["Chess Club"]["participants"].count(email) == 1


def test_signup_rejects_when_activity_is_full(client):
    activity = activities["Chess Club"]
    activity["participants"] = [f"s{i}@mergington.edu" for i in range(activity["max_participants"])]

    response = client.post("/activities/Chess Club/signup", params={"email": "late@mergington.edu"})

    assert response.status_code == 400
    assert "late@mergington.edu" not in activity["participants"]


def test_signup_succeeds_for_new_student(client):
    response = client.post("/activities/Gym Class/signup", params={"email": "new@mergington.edu"})

    assert response.status_code == 200
    assert "new@mergington.edu" in activities["Gym Class"]["participants"]
