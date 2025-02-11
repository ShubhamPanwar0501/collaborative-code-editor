from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    response = client.post("/users/register", json={"username": "testuser", "email": "test@domain.com", "password": "password"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_login_user():
    client.post("/users/register", json={"username": "testuser", "email": "test@domain.com", "password": "password"})
    response = client.post("/users/token", data={"username": "testuser", "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json()
