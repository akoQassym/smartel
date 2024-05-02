from app import app
from fastapi.testclient import TestClient
from dotenv import load_dotenv

import os
import sys
import io
import asyncio

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


client = TestClient(app)
load_dotenv()

USER_ID = os.getenv("USER_ID")
NON_EXISTING_ID = os.getenv("NON_EXISTING_ID")
APPOINTMENT_ID = os.getenv("APPOINTMENT_ID")
DOCUMENT_ID = os.getenv("DOCUMENT_ID")


# normal register user
def test_register():
    response = client.post(
        "/register",
        json={
            "user_id": "testing_script_id04",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        }
    )

    if response.status_code == 201:
        print("Successfully created new User")
    else:
        print("Test case failed")

def test_get_user():
    # You must ensure that the user with this ID exists in your test database
    user_id = USER_ID
    response = client.get(f"/user/{user_id}")
    assert response.status_code == 200
    assert response.json()["user_id"] == user_id

def test_get_user_not_found():
    # Use a non-existent user ID
    user_id = NON_EXISTING_ID
    response = client.get(f"/user/{user_id}")
    assert response.status_code == 404


def test_get_user():
    # You must ensure that the user with this ID exists in your test database
    user_id = USER_ID
    response = client.get(f"/user/{user_id}")
    assert response.status_code == 200
    assert response.json()["user_id"] == user_id

def test_get_user_not_found():
    # Use a non-existent user ID
    user_id = NON_EXISTING_ID
    response = client.get(f"/user/{user_id}")
    assert response.status_code == 404

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
    os.environ['TESTING'] = 'True'  # Example environment control
    if os.getenv('TESTING') == 'True':
        sys.stdout = io.StringIO()

    test_register()
    # test_get_user()
    # test_get_user_not_found()
    # test_create_patient()
    # test_get_physician()
    # test_get_physician_not_found()
    # test_book_appointment()
    # test_book_appointment_failed()
    # print("All tests passed successfully!")