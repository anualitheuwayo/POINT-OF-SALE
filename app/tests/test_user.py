def test_list_users(client):
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_user(client):
    user_data = {
        "full_name": "Admin User",
        "username": "admin",
        "role": "admin",
        "email": "admin@example.com",
        "is_active": True,
        "password": "securepassword123",
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    assert response.json()["username"] == user_data["username"]
    assert response.json()["role"] == user_data["role"]
    assert "password" not in response.json()
    user_id = response.json()["user_id"]


def test_get_user(client):
    user_data = {
        "full_name": "Cashier User",
        "username": "cashier",
        "role": "cashier",
        "email": "cashier@example.com",
        "is_active": True,
        "password": "password123",
    }
    create_response = client.post("/users", json=user_data)
    assert create_response.status_code == 201
    user_id = create_response.json()["user_id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["username"] == user_data["username"]
    assert "password" not in response.json()


def test_update_user(client):
    user_data = {
        "full_name": "Manager User",
        "username": "manager",
        "role": "manager",
        "email": "manager@example.com",
        "is_active": True,
        "password": "password123",
    }
    create_response = client.post("/users", json=user_data)
    assert create_response.status_code == 201
    user_id = create_response.json()["user_id"]

    update_data = {"full_name": "Senior Manager", "role": "admin"}
    response = client.put(f"/users/{user_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["full_name"] == update_data["full_name"]
    assert response.json()["role"] == update_data["role"]


def test_delete_user(client):
    user_data = {
        "full_name": "Temp User",
        "username": "tempuser",
        "role": "cashier",
        "email": "temp@example.com",
        "is_active": True,
        "password": "temppassword",
    }
    create_response = client.post("/users", json=user_data)
    assert create_response.status_code == 201
    user_id = create_response.json()["user_id"]

    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204

    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404


def test_get_nonexistent_user(client):
    response = client.get("/users/99999")
    assert response.status_code == 404


def test_create_user_missing_required_fields(client):
    response = client.post("/users", json={"username": "missing_fields"})
    assert response.status_code == 422


def test_create_user_duplicate_username(client):
    user_data = {
        "full_name": "User 1",
        "username": "duplicate",
        "role": "cashier",
        "email": "user1@example.com",
        "is_active": True,
        "password": "password123",
    }
    resp1 = client.post("/users", json=user_data)
    assert resp1.status_code == 201

    user_data["email"] = "user2@example.com"
    user_data["full_name"] = "User 2"
    resp2 = client.post("/users", json=user_data)
    assert resp2.status_code == 400


def test_create_user_invalid_email(client):
    user_data = {
        "full_name": "Test",
        "username": "testuser",
        "role": "cashier",
        "email": "invalid-email",
        "is_active": True,
        "password": "password123",
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 422


def test_update_nonexistent_user(client):
    response = client.put("/users/99999", json={"full_name": "Updated"})
    assert response.status_code == 404


def test_delete_nonexistent_user(client):
    response = client.delete("/users/99999")
    assert response.status_code == 404