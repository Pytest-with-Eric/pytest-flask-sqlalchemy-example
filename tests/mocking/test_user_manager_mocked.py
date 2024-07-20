# import json
# from user_manager.models import User


# def test_add_user(test_client, user_payload, mocker):
#     # Mock the add and commit operations
#     mock_session_add = mocker.patch("user_manager.models.db.session.add", autospec=True)
#     mock_session_commit = mocker.patch(
#         "user_manager.models.db.session.commit", autospec=True
#     )

#     # Mock the User.query.all() method to return an empty list initially
#     mock_user_query_all = mocker.patch(
#         "user_manager.models.User.query.all", return_value=[]
#     )

#     # Simulate the POST request to add a user
#     response = test_client.post(
#         "/users", data=json.dumps(user_payload), content_type="application/json"
#     )
#     assert response.status_code == 201
#     create_response_json = json.loads(response.data)
#     assert create_response_json == {"message": "User created"}

#     # Ensure that the session operations were called correctly
#     mock_session_add.assert_called_once()
#     mock_session_commit.assert_called_once()

#     # Create a new User instance
#     new_user = User(username=user_payload["username"], email=user_payload["email"])

#     # Now mock the User.query.all() method to return the new user
#     mock_user_query_all.return_value = [new_user]

#     # Simulate the GET request to fetch users
#     response = test_client.get("/users")
#     assert response.status_code == 200
#     read_response_json = json.loads(response.data)
#     assert read_response_json == [
#         {
#             "id": None,
#             "username": user_payload["username"],
#             "email": user_payload["email"],
#         }
#     ]
