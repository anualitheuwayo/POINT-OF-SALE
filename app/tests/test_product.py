from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_list_products():
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
def test_create_product():
    product_data = {
        "name": "Cocal Cola",
        "price": 100,
        "category_id": 1,
    }
    response = client.post("/products", json=product_data)
    assert response.status_code == 201
    assert response.json()["name"] == product_data["name"]
    assert response.json()["price"] == product_data["price"]
    assert response.json()["category_id"] == product_data["category_id"]