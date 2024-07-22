import json
from user_manager.models import User


def test_add_user(test_client, user_payload, mocker):
    # Mock the add and commit operations
    mock_session_add = mocker.patch("user_manager.app.db.session.add", autospec=True)
    mock_session_commit = mocker.patch(
        "user_manager.app.db.session.commit", autospec=True
    )

    # Simulate the POST request to add a user
    response = test_client.post(
        "/users", data=json.dumps(user_payload), content_type="application/json"
    )
    assert response.status_code == 201
    create_response_json = json.loads(response.data)
    assert create_response_json == {"message": "User created"}

    # Ensure that the session operations were called correctly
    mock_session_add.assert_called_once()
    mock_session_commit.assert_called_once()

    # Mock User.query to return a list containing a new User instance
    mock_user_query = mocker.patch("user_manager.app.User.query")
    expected_user_object = User(
        username=user_payload["username"], email=user_payload["email"]
    )
    mock_user_query.all.return_value = [expected_user_object]

    # Simulate the GET request to fetch users
    response = test_client.get("/users")
    assert response.status_code == 200
    read_response_json = json.loads(response.data)

    # assert that query.all() was called
    mock_user_query.all.assert_called_once()
    assert read_response_json == [
        {
            "id": None,  # ID is None because the User instance isn't saved to a real DB
            "username": user_payload["username"],
            "email": user_payload["email"],
        }
    ]
