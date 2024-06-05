from app import app
from fastapi.testclient import TestClient
from dotenv import load_dotenv

import pytest
import os
import uuid
import sys
import asyncio
import json

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


client = TestClient(app)
load_dotenv()

USER_ID = os.getenv("USER_ID")
NON_EXISTING_ID = os.getenv("NON_EXISTING_ID")
APPOINTMENT_ID = os.getenv("APPOINTMENT_ID")
DOCUMENT_ID = os.getenv("DOCUMENT_ID")
SPECIALIZATION_ID = os.getenv("SPECIALIZATION_ID")

# with open("outcome.json", "r") as f:
#     outcomes = json.load(f)

outcomes = {}

def save_outcomes(test_name, success):
    if success:
        outcomes[test_name] = "success"
    else:
        outcomes[test_name] = "fail"

    with open("outcomes.json", "a") as f:    
        json.dump(outcomes, f)

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
def test_get_non_existent_user():
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
            "birth_date": "2024-04-12T14:30:00",
            "blood_type": "The blood type of the patient",
            "height": "The height of the patient",
            "phone_number": "The phone number of the user",
            "sex": "Can be male, female, or other",
            "weight": "The weight of the patient"
        }
    )
    
    save_outcomes("create_patient", response.status_code < 300)

def test_get_physician():
    user_id = USER_ID
    response = client.get(f"/user/physician/{user_id}")
    save_outcomes("get_physician", response.status_code < 300)

def test_get_non_existent_physician():
    user_id = NON_EXISTING_ID
    response = client.get(f"/user/physician/{user_id}")
    save_outcomes("get_non_existant_user", response.status_code > 300)

def test_register_physician():
    response = client.post(
        "/register/physician",
        json={
            "user_id": USER_ID,
            "specialization_id": SPECIALIZATION_ID,
            "phone_number": "test_phone_number",
            "sex": "test_sex",
            "birth_date": "test_birth_date",
        }
    )

    save_outcomes("register_physician", response.status_code < 300)

def test_edit_user():
    user_id = USER_ID
    response = client.post(
        f"/edit_user/{user_id}",
        json={
            "sex": "Can be male, female, or other"
        }
    )

    save_outcomes("edit_user", response.status_code < 300)

def test_add_specialization():
    user_id = USER_ID
    response = client.post(
        f"/add_specialization/{user_id}",
        json={
            "description": "Test Specialization",
            "name": "Test Specialization",
        }
    )

    save_outcomes("add_specialization", response.status_code > 300)

def test_get_specialization():
    response = client.get(f"/specializations")
    save_outcomes("get_specialization", response.status_code > 300)

def test_add_appointment():
    physician_id = USER_ID
    response = client.post(
        f"/add_appointment/{physician_id}",
        json={
            "physician_id": physician_id,
            "start_time": "2022-01-01 10:30:00"
        }
    )
    
    save_outcomes("add_appointment", response.status_code > 300)

def test_get_available_appointments():
    specialization_id = SPECIALIZATION_ID
    response = client.get(f"/available_appointments/{specialization_id}")

    save_outcomes("get_available_appointments", response.status_code > 300)

def test_get_available_appointments_non_existent_id():
    specialization_id = NON_EXISTING_ID
    response = client.get(f"/available_appointments/{specialization_id}")

    save_outcomes("get_available_appointments_with_non-existent_id", response.status_code > 300)


# def test_delete_appointment():
#     appointment_id = APPOINTMENT_ID
#     response = client.delete(f"/appointment/{appointment_id}")
#     response = client.delete(f"/appointment/{appointment_id}")
#     save_outcomes("delete_appointment", response.status_code < 300)

def test_book_appointment():
    appointment_id = APPOINTMENT_ID
    patient_id = USER_ID
    response = client.post(f"/book_appointment/{appointment_id}/{patient_id}")

    save_outcomes("book_appointment", response.status_code > 300)

def test_book_non_existent_appointment():
    appointment_id = NON_EXISTING_ID
    patient_id = USER_ID
    response = client.post(f"/book_appointment/{appointment_id}/{patient_id}")
    save_outcomes("book_non_existent_appointment", response.status_code > 300)


def test_summarize_transcription():
    appointment_id = APPOINTMENT_ID
    response = client.post(f"/summarize_transcription/{appointment_id}")

    save_outcomes("summarize_transcription", response.status_code > 300)

def test_non_existent_summarize_transcription():
    appointment_id = NON_EXISTING_ID
    response = client.post(f"/summarize_transcription/{appointment_id}")

    save_outcomes("summarize_non_existent_transcription", response.status_code > 300)


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
    
    save_outcomes("get_summary", response.status_code > 300)

def test_get_non_existent_summary():
    document_id = NON_EXISTING_ID
    response = client.get(f"/summary/{document_id}")
    
    save_outcomes("get_summary_failed", response.status_code >= 300)



if __name__ == "__main__":
    # test_register()
    # test_register()
    # test_get_user()
    # test_get_non_existent_user()
    # test_create_patient()
    # test_get_physician()
    # test_get_non_existent_physician()
    # test_register_physician()
    # test_edit_user()
    # test_add_specialization()
    # test_get_specialization()
    # test_add_appointment()
    # test_get_available_appointments()
    # test_get_available_appointments_non_existent_id()
    # test_delete_appointment()
    # test_book_appointment()
    # test_book_non_existent_appointment()
    # test_summarize_transcription()
    # test_non_existent_summarize_transcription()
    # test_transcribe_and_summarize()
    # test_review_edit()
    # test_get_summary()
    # test_get_non_existent_summary()

    msg = '''Printing the test log:
    (test_case_name: success)" means that system responded as expected
    (test_case_name: fail) means that system did not respond as expected \n\n'''
    print(msg)

    # for key, value in outcomes.items():
    #     print(f"({key}: {value})")