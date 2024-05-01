# This file will act as the entry point for your application. It will initialize
# the app and database connections, define routes, and include any configuration
# settings.

# standard library
from http.client import HTTPException
from fastapi import FastAPI, Query, Body, Request
import tempfile
from fastapi import File, UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from http import HTTPStatus
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from dotenv import load_dotenv
from openai import OpenAI

import openai
import uuid
import httpx
import asyncio
import os 

# local library
from crud import CRUD
from base import engine
from models import User, Patient, Physician, Specialization, Appointment, SummaryDocument
from schemas import UserCreateModel, PatientCreateModel, PhysicianCreateModel, SpecializationCreateModel, AppointmentCreateModel, SummaryDocumentCreateModel

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")

if OPENAI_KEY is None:
    raise ValueError("OPENAI_KEY not found in environment variables")

openAIClient = OpenAI(api_key=OPENAI_KEY)

app = FastAPI(
    title = "Smartel API",
    description = "API for Smartel",
    docs_url = "/",
)

# Allow requests from all origins with appropriate methods and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "*"],  # You can specify specific origins instead of "*" for production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

async_session = async_sessionmaker(
        bind = engine,
        expire_on_commit = False,
    )

# creating instances of CRUD for each model
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

    user = await crud_user.create(new_user, async_session)
    return user

@app.get('/user/{user_id}', status_code=HTTPStatus.OK)
async def get_user(user_id: str):
    res = await crud_user.get_one(async_session, filter = {"user_id": user_id})
    return res

@app.get('/user/patient/{user_id}', status_code=HTTPStatus.OK)
async def get_patient(user_id: str):
    res = await crud_patient.get_one(async_session, filter = {"user_id": user_id})
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

    patient = await crud_patient.create(new_patient, async_session)
    return patient

@app.get('/user/physician/{user_id}', status_code=HTTPStatus.OK)
async def get_physician(user_id: str):
    res = await crud_physician.get_one(async_session, filter = {"user_id": user_id})
    return res

@app.post('/register/physician/{user_id}', status_code=HTTPStatus.CREATED)
async def create_physician(user_id: str, physician_data: PhysicianCreateModel):
    new_physician = Physician(
        user_id = user_id,
        specialization_id = physician_data.specialization_id,
        phone_number = physician_data.phone_number,
        sex = physician_data.sex,
        birth_date = physician_data.birth_date,
    )

    physician = await crud_physician.create(new_physician, async_session)
    return physician

@app.patch('/edit/{user_id}', status_code=HTTPStatus.OK)
async def edit_user(
    user_id: str, 
    patient_data: Optional[PatientCreateModel] = Body(default=None),
    physician_data: Optional[PhysicianCreateModel] = Body(default=None)
):

    # Check and update patient
    if patient_data:
        updated_patient = await crud_patient.update(patient_data.dict(exclude_unset=True), async_session, {"user_id": user_id})
        if updated_patient:
            return {"message": "Patient updated successfully", "data": updated_patient}
    
    # Check and update physician
    if physician_data:
        updated_physician = await crud_physician.update(physician_data.dict(exclude_unset=True), async_session, {"user_id": user_id})
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

    spec = await crud_specialization.create(new_specialization, async_session)
    return spec

@app.get('/get_specializations', status_code=HTTPStatus.OK)
async def get_specializations():
    specializations = await crud_specialization.get_all(async_session)
    return specializations


# ------ APIS FOR APPOINTMENTS ------ #
@app.post('/add_appointment/{physician_id}', status_code=HTTPStatus.CREATED)   
async def add_appointment(physician_id: str, appointment_data: AppointmentCreateModel): 
    new_appointment = Appointment(
        physician_id = physician_id,
        start_date_time = appointment_data.start_date_time,
    )

    appointment = await crud_appointment.create(new_appointment, async_session)
    return appointment

@app.get('/get_appointments/{physician_id}', status_code=HTTPStatus.OK)
async def get_appointments(physician_id: str):
    appointments = await crud_appointment.get_all(async_session, filter = {"physician_id": physician_id})
    return appointments

@app.post('/edit_appointment/{appointment_id}', status_code=HTTPStatus.OK)
async def edit_appointment(appointment_id: str, appointment_data: AppointmentCreateModel):
    updated_appointment = await crud_appointment.update(appointment_data.dict(exclude_unset=True), async_session, {"appointment_id": appointment_id})
    return updated_appointment

@app.delete('/delete_appointment/{appointment_id}', status_code=HTTPStatus.OK)
async def delete_appointment(appointment_id: str):
    deleted = await crud_appointment.delete(appointment_id, async_session)
    return {"message": "Appointment deleted successfully", "data": deleted}

@app.post('/book_appointment/{appointment_id}/{patient_id}', status_code=HTTPStatus.OK)
async def book_appointment(appointment_id: str, patient_id: str):
    appointment = await crud_appointment.get_one(async_session, filter = {"appointment_id": appointment_id})
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    update_data = {'isBooked': True, 'patient_id': patient_id}
    updated_appointment = await crud_appointment.update(update_data, async_session, {"appointment_id": appointment_id})
    
    if not updated_appointment:
        raise HTTPException(status_code=404, detail="Failed to update the appointment")
    
    return {"message": "Appointment booked successfully", "appointment": updated_appointment}

# ------ APIS FOR GENERATING DOCUMENTS ------ #
@app.post('/transcribe_audio/', status_code=HTTPStatus.CREATED)
async def transcribe_audio(audio_file: UploadFile = File(...)):
    try:
        # Create a temporary file to save the uploaded audio
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio_file:
            # Write the audio data from the blob to the temporary file
            temp_audio_file.write(await audio_file.read())
            temp_audio_file.close()

            # Transcribe the audio using the OpenAI API
            transcription = openAIClient.audio.transcriptions.create(
                model="whisper-1", 
                file=open(temp_audio_file.name, 'rb')
            )
            
            # Return the transcription text
            return {"transcription": transcription.text}
    except Exception as e:
        print("error when transcribing", e)
        raise HTTPException(status_code=404, detail="failed to transcribe")

@app.post('/summarize_transcription/{summary_doc_id}', status_code=HTTPStatus.OK)
async def summarize_transcription(summary_doc_id: str):
    result = await crud_summary_document.get_one(async_session, filter={"summary_doc_id": summary_doc_id})
    transcription = result.transcription
    systemMessage = f'''
        You will be provided with a transcription (delimited with XML tags) of a consultation session between a patient 
        and a doctor, in particular, P refers to the patient and D refers to the doctor. The transcription is as follows:
    '''
    userMessage = f'''
        <transcription> {transcription} </transcription>

        The summary of the transcription should include the following sections:
        1. Reason for Consultation: This section sets the stage for the entire visit and should succinctly describe why the patient sought medical attention.
        2. Examination Findings: This section documents the findings from the physical examination and any diagnostic tests ordered during the consultation. 
        3. Assessment and Plan: This critical section provides a summary of the healthcare provider’s clinical assessment and the planned course of action. 
        4. Conclusion: The conclusion summarizes the consultation and outlines the follow-up plan.

        Please write 150 words for each section of the summary. If the information is not available, please write "Information not available".
    '''

    try:
        print("Requesting OpenAI API")
        async with httpx.AsyncClient() as client:
            response = openAIClient.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": systemMessage},
                    {"role": "user", "content": userMessage}
                ]
            )
            # update the summary document with the summary
            content = response.choices[0].message.content
            try:
                await crud_summary_document.update({"markdown_summary": content}, async_session, {"summary_doc_id": summary_doc_id})
            except Exception as e:
                print(f"An error occurred: {e}")
            print(response)
            return(response)

    except Exception as e:
        print(f"An error occurred: {e}")
    
@app.post("/transcribe_and_summarize/{appointment_id}", status_code=HTTPStatus.CREATED)
async def transcribe_and_summarize(appointment_id: str, audio_file: UploadFile = File(...)):
    # Transcribe the audio
    try:
        # Create a temporary file to save the uploaded audio
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio_file:
            # Write the audio data from the blob to the temporary file
            temp_audio_file.write(await audio_file.read())
            temp_audio_file.close()

            # Transcribe the audio using the OpenAI API
            transcription = openAIClient.audio.transcriptions.create(
                model="whisper-1", 
                file=open(temp_audio_file.name, 'rb')
            )
            
    except Exception as e:
        print("error when transcribing", e)
        raise HTTPException(status_code=404, detail="failed to transcribe")
    
    # Get the summary 
    systemMessage = f'''
        You will be provided with a transcription (delimited with XML tags) of a consultation session between a patient 
        and a doctor, in particular, P refers to the patient and D refers to the doctor. The transcription is as follows:
    '''
    userMessage = f'''
        <transcription> {transcription} </transcription>

        The summary of the transcription should include the following sections:
        1. Reason for Consultation: This section sets the stage for the entire visit and should succinctly describe why the patient sought medical attention.
        2. Examination Findings: This section documents the findings from the physical examination and any diagnostic tests ordered during the consultation. 
        3. Assessment and Plan: This critical section provides a summary of the healthcare provider’s clinical assessment and the planned course of action. 
        4. Conclusion: The conclusion summarizes the consultation and outlines the follow-up plan.

        Please write 150 words for each section of the summary. If the information is not available, please write "Information not available".
    '''

    try:
        print("Requesting OpenAI API")
        async with httpx.AsyncClient() as client:
            response = openAIClient.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": systemMessage},
                    {"role": "user", "content": userMessage}
                ]
            )

    except Exception as e:
        print(f"An error occurred: {e}")

    new_summary_doc = SummaryDocument(
        appointment_id = appointment_id,
        transcription = transcription.text,
        markdown_summary = response.choices[0].message.content,
    )

    summary_doc = await crud_summary_document.create(new_summary_doc, async_session)
    return summary_doc

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
    summarize_transcription(summary_doc_id)
'''