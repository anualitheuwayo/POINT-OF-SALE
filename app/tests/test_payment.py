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


def test_list_payments(client):
    response = client.get("/payments")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_payments_by_sale(client):
    sale_id = setup_test_data(client)

    response = client.get(f"/payments/sale/{sale_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1
    assert response.json()[0]["payment_method"] == "Cash"


def test_update_payment(client):
    sale_id = setup_test_data(client)

    payments_response = client.get(f"/payments/sale/{sale_id}")
    assert payments_response.status_code == 200
    payment_id = payments_response.json()[0]["payment_id"]

    update_data = {"status": "Refunded", "transaction_ref": "REF-12345"}
    response = client.put(f"/payments/{payment_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["status"] == "Refunded"
    assert response.json()["transaction_ref"] == "REF-12345"


def test_get_nonexistent_payment(client):
    response = client.get("/payments/99999")
    assert response.status_code == 404


def test_get_payments_for_nonexistent_sale(client):
    response = client.get("/payments/sale/99999")
    assert response.status_code == 404


def test_update_nonexistent_payment(client):
    response = client.put("/payments/99999", json={"status": "Refunded"})
    assert response.status_code == 404


def test_create_payment_invalid_sale(client):
    payment_data = {"payment_method": "Card", "amount": "10.00"}
    response = client.post("/payments/sale/99999", json=payment_data)
    assert response.status_code == 404


def test_create_payment_missing_fields(client):
    response = client.post("/payments/sale/1", json={"amount": "10.00"})
    assert response.status_code == 422