from app import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_register():
    response = client.post(
        "/register",
        json={
            "user_id": "unique_user_id",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        }
    )
    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully"}

def test_get_user():
    # You must ensure that the user with this ID exists in your test database
    user_id = "existing_user_id"
    response = client.get(f"/user/{user_id}")
    assert response.status_code == 200
    assert response.json()["user_id"] == user_id

def test_get_user_not_found():
    # Use a non-existent user ID
    user_id = "nonexistent_user_id"
    response = client.get(f"/user/{user_id}")
    assert response.status_code == 404


def test_get_user():
    # You must ensure that the user with this ID exists in your test database
    user_id = "existing_user_id"
    response = client.get(f"/user/{user_id}")
    assert response.status_code == 200
    assert response.json()["user_id"] == user_id

def test_get_user_not_found():
    # Use a non-existent user ID
    user_id = "nonexistent_user_id"
    response = client.get(f"/user/{user_id}")
    assert response.status_code == 404

def test_create_patient():
    user_id = "existing_user_id"
    response = client.post(
        f"/register/patient/{user_id}",
        json={
            "height": 180,
            "weight": 75,
            "phone_number": "1234567890",
            "sex": "male",
            "birth_date": "1990-01-01",
            "blood_type": "O+"
        }
    )
    assert response.status_code == 201
    assert response.json()["user_id"] == user_id

def test_get_physician():
    user_id = "existing_physician_id"
    response = client.get(f"/user/physician/{user_id}")
    assert response.status_code == 200
    assert response.json()["user_id"] == user_id

def test_get_physician_not_found():
    user_id = "nonexistent_physician_id"
    response = client.get(f"/user/physician/{user_id}")
    assert response.status_code == 404

def test_book_appointment():
    appointment_id = "available_appointment_id"
    patient_id = "existing_patient_id"
    response = client.post(f"/book_appointment/{appointment_id}/{patient_id}")
    assert response.status_code == 200
    assert "Appointment booked successfully" in response.json()["message"]

def test_book_appointment_failed():
    appointment_id = "nonexistent_appointment_id"
    patient_id = "existing_patient_id"
    response = client.post(f"/book_appointment/{appointment_id}/{patient_id}")
    assert response.status_code == 404

