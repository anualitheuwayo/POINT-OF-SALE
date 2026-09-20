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

    return product_id, customer_id, user_id


def test_list_sales(client):
    response = client.get("/sales")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_sale(client):
    product_id, customer_id, user_id = setup_test_data(client)

    sale_data = {
        "customer_id": customer_id,
        "user_id": user_id,
        "discount_amount": "0.00",
        "sale_items": [
            {
                "product_id": product_id,
                "quantity": 2,
                "line_discount": "0.00",
            }
        ],
        "payments": [
            {
                "payment_method": "Cash",
                "amount": "20.00",
            }
        ],
    }
    response = client.post("/sales", json=sale_data)
    assert response.status_code == 201
    assert response.json()["customer_id"] == customer_id
    assert response.json()["user_id"] == user_id
    assert len(response.json()["sale_items"]) == 1
    assert len(response.json()["payments"]) == 1
    sale_id = response.json()["sale_id"]


def test_get_sale(client):
    product_id, customer_id, user_id = setup_test_data(client)

    sale_data = {
        "customer_id": customer_id,
        "user_id": user_id,
        "discount_amount": "0.00",
        "sale_items": [
            {"product_id": product_id, "quantity": 1, "line_discount": "0.00"}
        ],
        "payments": [
            {"payment_method": "Card", "amount": "10.00"}
        ],
    }
    create_response = client.post("/sales", json=sale_data)
    assert create_response.status_code == 201
    sale_id = create_response.json()["sale_id"]

    response = client.get(f"/sales/{sale_id}")
    assert response.status_code == 200
    assert response.json()["sale_id"] == sale_id


def test_update_sale(client):
    product_id, customer_id, user_id = setup_test_data(client)

    sale_data = {
        "customer_id": customer_id,
        "user_id": user_id,
        "discount_amount": "0.00",
        "sale_items": [
            {"product_id": product_id, "quantity": 1, "line_discount": "0.00"}
        ],
        "payments": [
            {"payment_method": "Cash", "amount": "10.00"}
        ],
    }
    create_response = client.post("/sales", json=sale_data)
    assert create_response.status_code == 201
    sale_id = create_response.json()["sale_id"]

    update_data = {"status": "Completed"}
    response = client.put(f"/sales/{sale_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["status"] == "Completed"


def test_get_nonexistent_sale(client):
    response = client.get("/sales/99999")
    assert response.status_code == 404


def test_create_sale_invalid_user(client):
    product_id, customer_id, user_id = setup_test_data(client)

    sale_data = {
        "customer_id": customer_id,
        "user_id": 99999,
        "discount_amount": "0.00",
        "sale_items": [
            {"product_id": product_id, "quantity": 1, "line_discount": "0.00"}
        ],
        "payments": [
            {"payment_method": "Cash", "amount": "10.00"}
        ],
    }
    response = client.post("/sales", json=sale_data)
    assert response.status_code == 400


def test_create_sale_invalid_customer(client):
    product_id, customer_id, user_id = setup_test_data(client)

    sale_data = {
        "customer_id": 99999,
        "user_id": user_id,
        "discount_amount": "0.00",
        "sale_items": [
            {"product_id": product_id, "quantity": 1, "line_discount": "0.00"}
        ],
        "payments": [
            {"payment_method": "Cash", "amount": "10.00"}
        ],
    }
    response = client.post("/sales", json=sale_data)
    assert response.status_code == 400


def test_create_sale_invalid_product(client):
    product_id, customer_id, user_id = setup_test_data(client)

    sale_data = {
        "customer_id": customer_id,
        "user_id": user_id,
        "discount_amount": "0.00",
        "sale_items": [
            {"product_id": 99999, "quantity": 1, "line_discount": "0.00"}
        ],
        "payments": [
            {"payment_method": "Cash", "amount": "10.00"}
        ],
    }
    response = client.post("/sales", json=sale_data)
    assert response.status_code == 404


def test_create_sale_insufficient_stock(client):
    product_id, customer_id, user_id = setup_test_data(client)

    sale_data = {
        "customer_id": customer_id,
        "user_id": user_id,
        "discount_amount": "0.00",
        "sale_items": [
            {"product_id": product_id, "quantity": 99999, "line_discount": "0.00"}
        ],
        "payments": [
            {"payment_method": "Cash", "amount": "999990.00"}
        ],
    }
    response = client.post("/sales", json=sale_data)
    assert response.status_code == 400


def test_create_sale_payment_mismatch(client):
    product_id, customer_id, user_id = setup_test_data(client)

    sale_data = {
        "customer_id": customer_id,
        "user_id": user_id,
        "discount_amount": "0.00",
        "sale_items": [
            {"product_id": product_id, "quantity": 1, "line_discount": "0.00"}
        ],
        "payments": [
            {"payment_method": "Cash", "amount": "5.00"}
        ],
    }
    response = client.post("/sales", json=sale_data)
    assert response.status_code == 400


def test_create_sale_missing_items(client):
    product_id, customer_id, user_id = setup_test_data(client)

    sale_data = {
        "customer_id": customer_id,
        "user_id": user_id,
        "discount_amount": "0.00",
        "sale_items": [],
        "payments": [
            {"payment_method": "Cash", "amount": "10.00"}
        ],
    }
    response = client.post("/sales", json=sale_data)
    assert response.status_code == 400


def test_create_sale_missing_payments(client):
    product_id, customer_id, user_id = setup_test_data(client)

    sale_data = {
        "customer_id": customer_id,
        "user_id": user_id,
        "discount_amount": "0.00",
        "sale_items": [
            {"product_id": product_id, "quantity": 1, "line_discount": "0.00"}
        ],
        "payments": [],
    }
    response = client.post("/sales", json=sale_data)
    assert response.status_code == 400


def test_update_nonexistent_sale(client):
    response = client.put("/sales/99999", json={"status": "Cancelled"})
    assert response.status_code == 404