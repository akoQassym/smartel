from app import app
from fastapi.testclient import TestClient
from dotenv import load_dotenv

import pytest
import os
import uuid
import sys
import asyncio

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


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
    
    save_outcomes("get_user", response.status_code < 300)

# get user by ID that does not exist
def test_get_non_existant_user():
    # Use a non-existent user ID
    user_id = NON_EXISTING_ID
    response = client.get(f"/user/{user_id}")
    # assert response.status_code == 404, "user_id found somehow"

    save_outcomes("get_non_existant_user", response.status_code > 300)

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
    
    save_outcomes("create_patient", response.status_code < 300)

def test_get_physician():
    user_id = USER_ID
    response = client.get(f"/user/physician/{user_id}")
    save_outcomes("get_physician", response.status_code < 300)

def test_get_non_existant_physician():
    user_id = NON_EXISTING_ID
    response = client.get(f"/user/physician/{user_id}")
    save_outcomes("get_non_existant_user", response.status_code > 300)

def test_book_appointment():
    appointment_id = APPOINTMENT_ID
    patient_id = USER_ID
    response = client.post(f"/book_appointment/{appointment_id}/{patient_id}")

    save_outcomes("book_appointment", response.status_code < 300)

def test_book_appointment_failed():
    appointment_id = NON_EXISTING_ID
    patient_id = USER_ID
    response = client.post(f"/book_appointment/{appointment_id}/{patient_id}")
    save_outcomes("book_appointment_failed", response.status_code > 300)


def test_summarize_transcription():
    appointment_id = APPOINTMENT_ID
    response = client.post(f"/summarize_transcription/{appointment_id}")

    save_outcomes("summarize_transcription", response.status_code < 300)

# def test_transcribe_and_summarize():
#     appointment_id = APPOINTMENT_ID
#     response = client.post(
#         f"/transcribe_and_summarize/{appointment_id}",
#         json={
#             "transcription": "This is a transcription"
#         }
#     )

#     save_outcomes("transcribe_and_summarize", response.status_code < 300)

# def test_review_edit():
#     document_id = DOCUMENT_ID
#     response = client.post(
#         f"/review/{document_id}",
#         json={
#             "review": "This is a review"
#         }
#     )
    
#     save_outcomes("review_edit", response.status_code < 300)

def test_get_summary():
    document_id = DOCUMENT_ID
    response = client.get(f"/summary/{document_id}")
    
    save_outcomes("get_summary", response.status_code < 300)

def test_get_summary_failed():
    document_id = NON_EXISTING_ID
    response = client.get(f"/summary/{document_id}")
    
    save_outcomes("get_summary_failed", response.status_code >= 300)



if __name__ == "__main__":
    # test_register() # working
    # test_get_user()
    test_get_non_existant_user()
    # test_create_patient()
    # test_get_physician()
    # test_get_physician_not_found()
    # test_book_appointment()
    # test_book_appointment_failed()
    # print("All tests passed successfully!")

    # if outcomes is None:
    #     print("All tests passed successfully!")

    msg = '''Printing the test log:
    (test_case_name: success)" means that system responded as expected
    (test_case_name: fail) means that system did not respond as expected \n\n'''
    print(msg)
    for key, value in outcomes.items():
        print(f"({key}: {value})")