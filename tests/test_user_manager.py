import json


def test_add_user(test_client, user_payload):
    response = test_client.post(
        "/users", data=json.dumps(user_payload), content_type="application/json"
    )
    assert response.status_code == 201
    create_response_json = json.loads(response.data)
    assert create_response_json == {"message": "User created"}

    response = test_client.get("/users")
    assert response.status_code == 200

    read_response_json = json.loads(response.data)
    print(read_response_json)
