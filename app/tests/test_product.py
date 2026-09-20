def test_list_products(client):
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_product(client):
    category_data = {"name": "Beverages", "description": "Drinks", "is_active": True}
    cat_response = client.post("/categories", json=category_data)
    assert cat_response.status_code == 201
    category_id = cat_response.json()["category_id"]

    supplier_data = {"company_name": "Coca Cola Company", "contact_email": "contact@coca-cola.com", "is_active": True}
    sup_response = client.post("/suppliers", json=supplier_data)
    assert sup_response.status_code == 201
    supplier_id = sup_response.json()["supplier_id"]

    product_data = {
        "sku": "COC-001",
        "name": "Coca Cola",
        "description": "Soft drink",
        "unit_price": "1.50",
        "cost_price": "0.75",
        "quantity_in_stock": 100,
        "reorder_level": 10,
        "category_id": category_id,
        "supplier_id": supplier_id,
        "is_active": True,
    }
    response = client.post("/products", json=product_data)
    assert response.status_code == 201
    assert response.json()["name"] == product_data["name"]
    assert response.json()["sku"] == product_data["sku"]
    assert response.json()["category_id"] == product_data["category_id"]


def test_create_product_duplicate_sku_fails(client):
    category_data = {"name": "Beverages", "description": "Drinks", "is_active": True}
    cat_response = client.post("/categories", json=category_data)
    category_id = cat_response.json()["category_id"]

    supplier_data = {"company_name": "Test Supplier", "contact_email": "test@supplier.com", "is_active": True}
    sup_response = client.post("/suppliers", json=supplier_data)
    supplier_id = sup_response.json()["supplier_id"]

    product_data = {
        "sku": "DUP-001",
        "name": "Product 1",
        "unit_price": "10.00",
        "cost_price": "5.00",
        "quantity_in_stock": 10,
        "category_id": category_id,
        "supplier_id": supplier_id,
        "is_active": True,
    }
    # Create first product
    resp1 = client.post("/products", json=product_data)
    assert resp1.status_code == 201

    # Try to create second with same SKU
    product_data["name"] = "Product 2"
    resp2 = client.post("/products", json=product_data)
    assert resp2.status_code == 400


def test_create_product_invalid_category(client):
    supplier_data = {"company_name": "Test Supplier", "contact_email": "test@supplier.com", "is_active": True}
    sup_response = client.post("/suppliers", json=supplier_data)
    supplier_id = sup_response.json()["supplier_id"]

    product_data = {
        "sku": "INV-001",
        "name": "Invalid Category Product",
        "unit_price": "10.00",
        "cost_price": "5.00",
        "quantity_in_stock": 10,
        "category_id": 99999,
        "supplier_id": supplier_id,
        "is_active": True,
    }
    response = client.post("/products", json=product_data)
    assert response.status_code == 400


def test_create_product_invalid_supplier(client):
    category_data = {"name": "Test Category", "description": "Test", "is_active": True}
    cat_response = client.post("/categories", json=category_data)
    category_id = cat_response.json()["category_id"]

    product_data = {
        "sku": "INV-002",
        "name": "Invalid Supplier Product",
        "unit_price": "10.00",
        "cost_price": "5.00",
        "quantity_in_stock": 10,
        "category_id": category_id,
        "supplier_id": 99999,
        "is_active": True,
    }
    response = client.post("/products", json=product_data)
    assert response.status_code == 400


def test_get_nonexistent_product(client):
    response = client.get("/products/99999")
    assert response.status_code == 404


def test_create_product_missing_required_fields(client):
    response = client.post("/products", json={"name": "Missing SKU"})
    assert response.status_code == 422


def test_create_product_invalid_price(client):
    category_data = {"name": "Test", "description": "Test", "is_active": True}
    cat_response = client.post("/categories", json=category_data)
    category_id = cat_response.json()["category_id"]

    supplier_data = {"company_name": "Test", "contact_email": "test@test.com", "is_active": True}
    sup_response = client.post("/suppliers", json=supplier_data)
    supplier_id = sup_response.json()["supplier_id"]

    product_data = {
        "sku": "INV-003",
        "name": "Invalid Price",
        "unit_price": "not-a-number",
        "cost_price": "5.00",
        "quantity_in_stock": 10,
        "category_id": category_id,
        "supplier_id": supplier_id,
        "is_active": True,
    }
    response = client.post("/products", json=product_data)
    assert response.status_code == 422


def test_update_nonexistent_product(client):
    response = client.put("/products/99999", json={"name": "Updated"})
    assert response.status_code == 404


def test_delete_nonexistent_product(client):
    response = client.delete("/products/99999")
    assert response.status_code == 404