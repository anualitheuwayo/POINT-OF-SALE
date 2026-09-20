def test_list_suppliers(client):
    response = client.get("/suppliers")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_supplier(client):
    supplier_data = {
        "company_name": "Tech Supplies Inc",
        "contact_name": "John Doe",
        "phone": "123-456-7890",
        "email": "john@techsupplies.com",
        "address": "123 Tech St, Silicon Valley",
        "is_active": True,
    }
    response = client.post("/suppliers", json=supplier_data)
    assert response.status_code == 201
    assert response.json()["company_name"] == supplier_data["company_name"]
    assert response.json()["contact_name"] == supplier_data["contact_name"]
    assert response.json()["email"] == supplier_data["email"]
    supplier_id = response.json()["supplier_id"]


def test_get_supplier(client):
    supplier_data = {
        "company_name": "Office World",
        "contact_name": "Jane Smith",
        "phone": "098-765-4321",
        "email": "jane@officeworld.com",
        "address": "456 Office Ave",
        "is_active": True,
    }
    create_response = client.post("/suppliers", json=supplier_data)
    assert create_response.status_code == 201
    supplier_id = create_response.json()["supplier_id"]

    response = client.get(f"/suppliers/{supplier_id}")
    assert response.status_code == 200
    assert response.json()["company_name"] == supplier_data["company_name"]


def test_update_supplier(client):
    supplier_data = {
        "company_name": "Food Distributors Ltd",
        "contact_name": "Bob Wilson",
        "phone": "555-123-4567",
        "email": "bob@fooddist.com",
        "address": "789 Food Blvd",
        "is_active": True,
    }
    create_response = client.post("/suppliers", json=supplier_data)
    assert create_response.status_code == 201
    supplier_id = create_response.json()["supplier_id"]

    update_data = {"company_name": "Food Distributors International", "contact_name": "Bob Wilson Jr", "is_active": True}
    response = client.put(f"/suppliers/{supplier_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["company_name"] == update_data["company_name"]
    assert response.json()["contact_name"] == update_data["contact_name"]


def test_delete_supplier(client):
    supplier_data = {
        "company_name": "Temp Supplier",
        "contact_name": "Temp Contact",
        "phone": "111-222-3333",
        "email": "temp@supplier.com",
        "address": "Temp Address",
        "is_active": True,
    }
    create_response = client.post("/suppliers", json=supplier_data)
    assert create_response.status_code == 201
    supplier_id = create_response.json()["supplier_id"]

    response = client.delete(f"/suppliers/{supplier_id}")
    assert response.status_code == 204

    get_response = client.get(f"/suppliers/{supplier_id}")
    assert get_response.status_code == 404


def test_get_nonexistent_supplier(client):
    response = client.get("/suppliers/99999")
    assert response.status_code == 404


def test_create_supplier_missing_required_fields(client):
    response = client.post("/suppliers", json={"contact_name": "Missing company"})
    assert response.status_code == 422


def test_create_supplier_invalid_email(client):
    response = client.post("/suppliers", json={
        "company_name": "Test", "email": "invalid-email", "is_active": True
    })
    assert response.status_code == 422


def test_update_nonexistent_supplier(client):
    response = client.put("/suppliers/99999", json={"company_name": "Updated"})
    assert response.status_code == 404


def test_delete_nonexistent_supplier(client):
    response = client.delete("/suppliers/99999")
    assert response.status_code == 404