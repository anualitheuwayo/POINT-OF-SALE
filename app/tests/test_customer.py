def test_list_customers(client):
    response = client.get("/customers")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_customer(client):
    customer_data = {
        "full_name": "Alice Johnson",
        "phone": "555-0101",
        "email": "alice@example.com",
        "loyalty_points": 0,
        "is_walk_in": False,
    }
    response = client.post("/customers", json=customer_data)
    assert response.status_code == 201
    assert response.json()["full_name"] == customer_data["full_name"]
    assert response.json()["email"] == customer_data["email"]
    customer_id = response.json()["customer_id"]


def test_get_customer(client):
    customer_data = {
        "full_name": "Bob Smith",
        "phone": "555-0202",
        "email": "bob@example.com",
        "loyalty_points": 100,
        "is_walk_in": False,
    }
    create_response = client.post("/customers", json=customer_data)
    assert create_response.status_code == 201
    customer_id = create_response.json()["customer_id"]

    response = client.get(f"/customers/{customer_id}")
    assert response.status_code == 200
    assert response.json()["full_name"] == customer_data["full_name"]


def test_update_customer(client):
    customer_data = {
        "full_name": "Carol White",
        "phone": "555-0303",
        "email": "carol@example.com",
        "loyalty_points": 50,
        "is_walk_in": False,
    }
    create_response = client.post("/customers", json=customer_data)
    assert create_response.status_code == 201
    customer_id = create_response.json()["customer_id"]

    update_data = {"full_name": "Carol Williams", "loyalty_points": 200}
    response = client.put(f"/customers/{customer_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["full_name"] == update_data["full_name"]
    assert response.json()["loyalty_points"] == update_data["loyalty_points"]


def test_delete_customer(client):
    customer_data = {
        "full_name": "Temp Customer",
        "phone": "555-9999",
        "email": "temp@example.com",
        "loyalty_points": 0,
        "is_walk_in": True,
    }
    create_response = client.post("/customers", json=customer_data)
    assert create_response.status_code == 201
    customer_id = create_response.json()["customer_id"]

    response = client.delete(f"/customers/{customer_id}")
    assert response.status_code == 204

    get_response = client.get(f"/customers/{customer_id}")
    assert get_response.status_code == 404


def test_get_nonexistent_customer(client):
    response = client.get("/customers/99999")
    assert response.status_code == 404


def test_create_customer_missing_required_fields(client):
    response = client.post("/customers", json={"phone": "555-0000"})
    assert response.status_code == 422


def test_create_customer_invalid_email(client):
    response = client.post("/customers", json={
        "full_name": "Test", "phone": "555-0000", "email": "invalid-email"
    })
    assert response.status_code == 422


def test_update_nonexistent_customer(client):
    response = client.put("/customers/99999", json={"full_name": "Updated"})
    assert response.status_code == 404


def test_delete_nonexistent_customer(client):
    response = client.delete("/customers/99999")
    assert response.status_code == 404