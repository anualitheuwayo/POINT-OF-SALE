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