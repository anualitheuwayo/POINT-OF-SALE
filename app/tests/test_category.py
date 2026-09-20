def test_list_categories(client):
    response = client.get("/categories")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_category(client):
    category_data = {"name": "Electronics", "description": "Electronic devices", "is_active": True}
    response = client.post("/categories", json=category_data)
    assert response.status_code == 201
    assert response.json()["name"] == category_data["name"]
    assert response.json()["description"] == category_data["description"]
    assert response.json()["is_active"] == category_data["is_active"]
    category_id = response.json()["category_id"]


def test_get_category(client):
    category_data = {"name": "Books", "description": "Books and magazines", "is_active": True}
    create_response = client.post("/categories", json=category_data)
    assert create_response.status_code == 201
    category_id = create_response.json()["category_id"]

    response = client.get(f"/categories/{category_id}")
    assert response.status_code == 200
    assert response.json()["name"] == category_data["name"]


def test_update_category(client):
    category_data = {"name": "Clothing", "description": "Apparel", "is_active": True}
    create_response = client.post("/categories", json=category_data)
    assert create_response.status_code == 201
    category_id = create_response.json()["category_id"]

    update_data = {"name": "Clothing & Accessories", "description": "Updated description", "is_active": True}
    response = client.put(f"/categories/{category_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["name"] == update_data["name"]
    assert response.json()["description"] == update_data["description"]


def test_delete_category(client):
    category_data = {"name": "Toys", "description": "Children toys", "is_active": True}
    create_response = client.post("/categories", json=category_data)
    assert create_response.status_code == 201
    category_id = create_response.json()["category_id"]

    response = client.delete(f"/categories/{category_id}")
    assert response.status_code == 204

    get_response = client.get(f"/categories/{category_id}")
    assert get_response.status_code == 404


def test_get_nonexistent_category(client):
    response = client.get("/categories/99999")
    assert response.status_code == 404


def test_create_category_missing_required_fields(client):
    response = client.post("/categories", json={"description": "Missing name"})
    assert response.status_code == 422


def test_create_category_invalid_is_active(client):
    response = client.post("/categories", json={"name": "Test", "description": "Test", "is_active": "not-a-bool"})
    assert response.status_code == 422


def test_update_nonexistent_category(client):
    response = client.put("/categories/99999", json={"name": "Updated"})
    assert response.status_code == 404


def test_delete_nonexistent_category(client):
    response = client.delete("/categories/99999")
    assert response.status_code == 404