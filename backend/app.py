# This file will act as the entry point for your application. It will initialize
# the app and database connections, define routes, and include any configuration
# settings.

# standard library
from http.client import HTTPException
from fastapi import FastAPI, Query, Body
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from http import HTTPStatus
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import uuid
import openai
import httpx
import asyncio
from dotenv import load_dotenv
import os 

# local library
from crud import CRUD
from base import engine
from models import User, Patient, Physician, Specialization, Appointment, SummaryDocument
from schemas import UserCreateModel, PatientCreateModel, PhysicianCreateModel, SpecializationCreateModel, AppointmentCreateModel, SummaryDocumentCreateModel


load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")

app = FastAPI(
    title = "Smartel API",
    description = "API for Smartel",
    docs_url = "/",
)

# Allow requests from all origins with appropriate methods and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify specific origins instead of "*" for production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

session = async_sessionmaker(
        bind = engine,
        expire_on_commit = False,
    )

# here use the CRUD class to interact with the database initializing class takes
# a good amount of time, so it is preferable to create a global instance to use
# it throughout the application
# crud_user = CRUD()
crud_user = CRUD(User)
crud_patient = CRUD(Patient)
crud_physician = CRUD(Physician)
crud_specialization = CRUD(Specialization)
crud_appointment = CRUD(Appointment)
crud_summary_document = CRUD(SummaryDocument)

@app.get("/")
async def root():
    return {"message": "Hello World"}


# ------ APIS FOR USERS ------ #
@app.post('/register', status_code=HTTPStatus.CREATED)
async def create_user(user_data: UserCreateModel): 
    new_user = User(
        user_id = user_data.user_id,
        first_name = user_data.first_name,
        last_name = user_data.last_name,
        email = user_data.email,
    )

    user = await crud_user.create(new_user, session)
    return user

@app.get('/user/{user_id}', status_code=HTTPStatus.OK)
async def get_user(user_id: str):
    res = await crud_user.get_one(user_id, session)
    return res

@app.get('/user/patient/{user_id}', status_code=HTTPStatus.OK)
async def get_patient(user_id: str):
    res = await crud_patient.get_one(user_id, session)
    return res

@app.post('/register/patient/{user_id}', status_code=HTTPStatus.CREATED)
async def create_patient(user_id: str, patient_data: PatientCreateModel):
    new_patient = Patient(
        user_id = user_id,
        height = patient_data.height,
        weight = patient_data.weight,
        phone_number = patient_data.phone_number,
        sex = patient_data.sex,
        birth_date = patient_data.birth_date,
        blood_type = patient_data.blood_type,
    )

    patient = await crud_patient.create(new_patient, session)
    return patient

@app.post('/register/physician/{user_id}', status_code=HTTPStatus.CREATED)
async def create_physician(user_id: str, physician_data: PhysicianCreateModel):
    new_physician = Physician(
        user_id = user_id,
        specialization_id = physician_data.specialization_id,
        phone_number = physician_data.phone_number,
        sex = physician_data.sex,
        birth_date = physician_data.birth_date,
    )

    physician = await crud_physician.create(new_physician, session)
    return physician

@app.patch('/edit/{user_id}', status_code=HTTPStatus.OK)
async def edit_user(
    user_id: str, 
    patient_data: Optional[PatientCreateModel] = Body(default=None),
    physician_data: Optional[PhysicianCreateModel] = Body(default=None)
):

    # Check and update patient
    if patient_data:
        updated_patient = await crud_patient.update(user_id, patient_data.dict(exclude_unset=True), session)
        if updated_patient:
            return {"message": "Patient updated successfully", "data": updated_patient}
    
    # Check and update physician
    if physician_data:
        updated_physician = await crud_physician.update(user_id, physician_data.dict(exclude_unset=True), session)
        if updated_physician:
            return {"message": "Physician updated successfully", "data": updated_physician}

    raise HTTPException(status_code=404, detail="No valid data provided or user not found")

# ------ APIS FOR SPECIALIZATION ------ #
@app.post('/add_specialization', status_code=HTTPStatus.CREATED)
async def add_spec(spec_data: SpecializationCreateModel): 
    new_specialization = Specialization(
        description = spec_data.description,
        name = spec_data.name,
    )

    spec = await crud_specialization.create(new_specialization, session)
    return spec

@app.get('/get_specializations', status_code=HTTPStatus.OK)
async def get_specializations():
    specializations = await crud_specialization.get_all(session)
    return specializations


# ------ APIS FOR APPOINTMENTS ------ #
@app.post('/add_appointment/{physician_id}', status_code=HTTPStatus.CREATED)   
async def add_appointment(physician_id: str, appointment_data: AppointmentCreateModel): 
    new_appointment = Appointment(
        physician_id = physician_id,
        start_date_time = appointment_data.start_date_time,
    )

    appointment = await crud_appointment.create(new_appointment, session)
    return appointment

@app.get('/get_appointments/{physician_id}', status_code=HTTPStatus.OK)
async def get_appointments(physician_id: str):
    appointments = await crud_appointment.get_all(session, filter = {"physician_id": physician_id})
    return appointments

@app.post('/edit_appointment/{appointment_id}', status_code=HTTPStatus.OK)
async def edit_appointment(appointment_id: str, appointment_data: AppointmentCreateModel):
    updated_appointment = await crud_appointment.update(appointment_id, appointment_data.dict(exclude_unset=True), session)
    return updated_appointment

@app.delete('/delete_appointment/{appointment_id}', status_code=HTTPStatus.OK)
async def delete_appointment(appointment_id: str):
    deleted = await crud_appointment.delete(appointment_id, session)
    return {"message": "Appointment deleted successfully", "data": deleted}

@app.post('/book_appointment/{appointment_id}/{patient_id}', status_code=HTTPStatus.OK)
async def book_appointment(appointment_id: str, patient_id: str):
    # Fetch the current appointment details
    appointment = await crud_appointment.get_one(appointment_id, session)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    # Update the appointment attributes
    update_data = {'isBooked': True, 'patient_id': patient_id}
    updated_appointment = await crud_appointment.update(appointment_id, update_data, session)
    
    if not updated_appointment:
        raise HTTPException(status_code=404, detail="Failed to update the appointment")
    
    return {"message": "Appointment booked successfully", "appointment": updated_appointment}

# ------ APIS FOR GENERATING DOCUMENTS ------ #
@app.post('transcribe_audio', status_code=HTTPStatus.CREATED)
async def transcribe_audio(audio_blob: str):
    pass

@app.post('/summarize_transcription/{document_id}', status_code=HTTPStatus.OK)
async def summarize_transcription(document_id: str):
    transcription = await crud_summary_document.get_one(document_id)
    
    # Create a prompt for the OpenAI API
    prompt = f'''
        You will be provided with a transcription (delimited with XML tags) of a consultation session between a patient 
        and a doctor, in particular, P refers to the patient and D refers to the doctor. The transcription is as follows:

        <transcription> {transcription} </transcription>

        The summary of the transcription should include the following sections:
        1. Reason for Consultation: This section sets the stage for the entire visit and should succinctly describe why the patient sought medical attention.
        2. Examination Findings: This section documents the findings from the physical examination and any diagnostic tests ordered during the consultation. 
        3. Assessment and Plan: This critical section provides a summary of the healthcare provider’s clinical assessment and the planned course of action. 
        4. Conclusion: The conclusion summarizes the consultation and outlines the follow-up plan.

        Please write 150 words for each section of the summary. If the information is not available, please write "Information not available".
    '''

    # Using OpenAI to generate a summary
    try:
        response = await httpx.post(
            "https://api.openai.com/v1/engines/davinci-codex/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_KEY}"
            },
            json={
                "prompt": prompt,
                "max_tokens": 150  # Adjust based on your needs
            }
        )
        response.raise_for_status()
        summary = response.json()['choices'][0]['text'].strip()
        return {"summary": summary}
    
    except httpx.HTTPError as error:
        raise HTTPException(status_code=error.response.status_code, detail="Failed to generate summary")


# ------ APIS FOR LOCAL USE ------ #
async def load_transcriptions(directory_path: str):
    print("Function called")
    # Path object for the directory
    from pathlib import Path

    path = Path(directory_path)

    print(f"Loading transcriptions from {path}")

    counter = 0
    if not path.exists():
        print(f"Directory {path} does not exist")
        return
    
    try:
        # Iterate over text files in the directory
        for file_path in path.glob('*.txt'):  # Adjust the pattern if necessary
            counter += 1
            if counter > 10:
                break
            
            # create a dummy string for the appointment_id
            appointment_id = "appointment_id_" + str(counter)
            appointment_id = str(uuid.uuid4())
            # Read the content of each file
            with open(file_path, 'r', encoding='utf-8') as file:
                transcription = file.read()

            # Create an instance of SummaryDocument
            summary_document = SummaryDocument(
                transcription = transcription,
                appointment_id = appointment_id  # This needs to be obtained or set appropriately
            )

            print(f"Appointment ID: {summary_document.appointment_id} is loaded into the database")

            # Use the CRUD class to save the transcription to the database
            await crud_summary_document.create(summary_document, session)

            print("Transcription loaded successfully")
    
    except Exception as e:
        print(f"An error occurred: {e}")

asyncio.run(load_transcriptions('./data/clean_transcript/'))


'''
    done: create_user(user_id, email)
    done: (implemented in a separate registration) add_patient_detail(user_id, first_name, last_name, age, sex, weight, height, blood_type)
    done: (implemented in a separate registration) add_physician_detail(user_id, first_name, last_name, age, sex, specialization_id)
    done: edit_physician(user_id, first_name, last_name, age, sex, specialization_id, type)
    done: edit_patient(user_id, first_name, last_name, age, sex, weight, height, blood_type)
    done: delete_user(user_id)
    done: get_specializations()
    done: get_appointments(physician_id) // returns all available appointments for that specialization
    done: add_appointment(date_time, phsyician_id, duration)
    done: edit_appointment(appointment_id, date_time, duration)
    done: delete_appointment(appointment_id)
    done: book_appointment(appointment_id)
    transcribe_audio(audio_blob)
    summarize_transcription(document_id)
'''