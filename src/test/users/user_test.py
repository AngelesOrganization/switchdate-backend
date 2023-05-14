
def test_create_user_should_return_200(postgres_container, client):
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "strong_password",
        "role": "user"
    }
    response = client.post("/users/", json=user_data)

    assert response.status_code == 200
    content = response.json()
    assert content is not None
    assert content["username"] == user_data["username"]
    assert content["email"] == user_data["email"]
    assert content["first_name"] == user_data["first_name"]
    assert content["last_name"] == user_data["last_name"]
    assert content["hashed_password"] == user_data["password"]
    assert content["role"] == user_data["role"]
