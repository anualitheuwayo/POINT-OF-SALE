def setup_test_data(client):
   
    cat_response = client.post("/categories", json={"name": "Test Category", "description": "Test", "is_active": True})
    category_id = cat_response.json()["category_id"]

  
    sup_response = client.post("/suppliers", json={"company_name": "Test Supplier", "email": "test@supplier.com", "is_active": True})
    supplier_id = sup_response.json()["supplier_id"]

    prod_response = client.post("/products", json={
        "sku": f"TEST-{category_id}-{supplier_id}",
        "name": "Test Product",
        "unit_price": "10.00",
        "cost_price": "5.00",
        "quantity_in_stock": 100,
        "category_id": category_id,
        "supplier_id": supplier_id,
        "is_active": True,
    })
    product_id = prod_response.json()["product_id"]

    cust_response = client.post("/customers", json={"full_name": "Test Customer", "email": "customer@test.com", "loyalty_points": 0, "is_walk_in": False})
    customer_id = cust_response.json()["customer_id"]

    user_response = client.post("/users", json={"full_name": "Test User", "username": f"testuser{customer_id}", "role": "cashier", "email": "user@test.com", "is_active": True, "password": "password123"})
    user_id = user_response.json()["user_id"]

    sale_response = client.post("/sales", json={
        "customer_id": customer_id,
        "user_id": user_id,
        "discount_amount": "0.00",
        "sale_items": [
            {"product_id": product_id, "quantity": 1, "line_discount": "0.00"}
        ],
        "payments": [
            {"payment_method": "Cash", "amount": "10.00"}
        ],
    })
    sale_id = sale_response.json()["sale_id"]

    return sale_id


def test_list_receipts(client):
    response = client.get("/receipts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_receipt(client):
    sale_id = setup_test_data(client)

    receipt_data = {"copy_type": "Original"}
    response = client.post(f"/receipts/sale/{sale_id}", json=receipt_data)
    assert response.status_code == 201
    assert response.json()["sale_id"] == sale_id
    assert response.json()["copy_type"] == "Original"
    assert response.json()["print_status"] == "Printed"
    receipt_id = response.json()["receipt_id"]


def test_get_receipt(client):
    sale_id = setup_test_data(client)

    create_response = client.post(f"/receipts/sale/{sale_id}", json={"copy_type": "Original"})
    assert create_response.status_code == 201
    receipt_id = create_response.json()["receipt_id"]

    response = client.get(f"/receipts/{receipt_id}")
    assert response.status_code == 200
    assert response.json()["receipt_id"] == receipt_id
    assert response.json()["sale_id"] == sale_id


def test_get_receipts_by_sale(client):
    sale_id = setup_test_data(client)

  
    client.post(f"/receipts/sale/{sale_id}", json={"copy_type": "Original"})

    response = client.get(f"/receipts/sale/{sale_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1