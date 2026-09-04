from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    print(response.json())
    print(response.status_code)
    print(response.headers)
    