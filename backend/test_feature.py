from app import app
from fastapi.testclient import TestClient
from dotenv import load_dotenv

import pytest
import uuid
import os

client = TestClient(app)
load_dotenv()

USER_ID = os.getenv("USER_ID")
NON_EXISTING_ID = os.getenv("NON_EXISTING_ID")
APPOINTMENT_ID = os.getenv("APPOINTMENT_ID")
DOCUMENT_ID = os.getenv("DOCUMENT_ID")

outcomes = {}

def save_outcomes(test_name, success):
    if success:
        outcomes[test_name] = "success"
    else:
        outcomes[test_name] = "fail"

# normal register user
def test_register():
    new_user_id = str(uuid.uuid4())
    response = client.post(
        "/register",
        json={
            "user_id": new_user_id,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        }
    )

    save_outcomes("register", response.status_code < 300)       

# get user by ID 
def test_get_user():
    # You must ensure that the user with this ID exists in your test database
    user_id = USER_ID
    response = client.get(f"/user/{user_id}")
    assert response.status_code == 200
    assert response.json()["user_id"] == user_id

# get user by ID that does not exist
def test_get_user_not_found():
    # Use a non-existent user ID
    user_id = NON_EXISTING_ID
    response = client.get(f"/user/{user_id}")
    # assert response.status_code == 404, "user_id found somehow"

    if response.status_code >= 300:
        outcomes["get_user"] = "success"
    
    else:
        outcomes["get_user"] = "fail"

# create a patient
def test_create_patient():
    user_id = USER_ID
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
    user_id = USER_ID
    response = client.get(f"/user/physician/{user_id}")
    assert response.status_code == 200
    assert response.json()["user_id"] == user_id

def test_get_physician_not_found():
    user_id = NON_EXISTING_ID
    response = client.get(f"/user/physician/{user_id}")
    assert response.status_code == 404

def test_book_appointment():
    appointment_id = APPOINTMENT_ID
    patient_id = USER_ID
    response = client.post(f"/book_appointment/{appointment_id}/{patient_id}")
    assert response.status_code == 200
    assert "Appointment booked successfully" in response.json()["message"]

def test_book_appointment_failed():
    appointment_id = NON_EXISTING_ID
    patient_id = USER_ID
    response = client.post(f"/book_appointment/{appointment_id}/{patient_id}")
    assert response.status_code == 404


if __name__ == "__main__":
    # test_register() # working
    # test_get_user()
    test_get_user_not_found()
    # test_create_patient()
    # test_get_physician()
    # test_get_physician_not_found()
    # test_book_appointment()
    # test_book_appointment_failed()
    # print("All tests passed successfully!")

    # if outcomes is None:
    #     print("All tests passed successfully!")

    for key, value in outcomes.items():
        print(f"{key}: {value}")