from src.app import activities


def test_signup_adds_new_student(client):
    # Arrange
    email = "new@mergington.edu"

    # Act
    response = client.post("/activities/Gym Class/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in activities["Gym Class"]["participants"]


def test_signup_rejects_unknown_activity(client):
    # Arrange
    email = "new@mergington.edu"

    # Act
    response = client.post("/activities/Nonexistent/signup", params={"email": email})

    # Assert
    assert response.status_code == 404


def test_signup_rejects_duplicate_email(client):
    # Arrange
    email = "new@mergington.edu"
    client.post("/activities/Chess Club/signup", params={"email": email})

    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert activities["Chess Club"]["participants"].count(email) == 1


def test_signup_rejects_when_activity_is_full(client):
    # Arrange
    activity = activities["Chess Club"]
    activity["participants"] = [f"s{i}@mergington.edu" for i in range(activity["max_participants"])]

    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": "late@mergington.edu"})

    # Assert
    assert response.status_code == 400
    assert "late@mergington.edu" not in activity["participants"]


def test_signup_accepts_last_available_spot(client):
    # Arrange
    activity = activities["Chess Club"]
    activity["participants"] = [f"s{i}@mergington.edu" for i in range(activity["max_participants"] - 1)]

    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": "last@mergington.edu"})

    # Assert
    assert response.status_code == 200
    assert len(activity["participants"]) == activity["max_participants"]
