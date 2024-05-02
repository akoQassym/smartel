from app import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_register():
    response = client.post(
        "/register",
        json={
            "username": "testuser",
            "password": "testpassword"
        }
    )
    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully"}

