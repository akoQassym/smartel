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
# from pandas import pd
from typing import List, Optional
import uuid

# local library
from crud import CRUD
from base import engine
from models import User, Patient, Physician, Specialization, Appointment, SummaryDocument
from schemas import UserCreateModel, PatientCreateModel, PhysicianCreateModel, SpecializationCreateModel, AppointmentCreateModel, SummaryDocumentCreateModel


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

@app.post('/register/patient/{user_id}', status_code=HTTPStatus.CREATED)
async def create_patient(user_id: str, patient_data: PatientCreateModel):
    new_patient = Patient(
        user_id = user_id,
        height = patient_data.height,
        weight = patient_data.weight,
        phone_number = patient_data.phone_number,
    )

    patient = await crud_patient.create(new_patient, session)
    return patient

@app.post('/register/physician/{user_id}', status_code=HTTPStatus.CREATED)
async def create_physician(user_id: str, physician_data: PhysicianCreateModel):
    new_physician = Physician(
        user_id = user_id,
        specialization_id = physician_data.specialization_id,
        phone_number = physician_data.phone_number,
    )

    physician = await crud_physician.create(new_physician, session)
    return physician

@app.post('/edit/{user_id}', status_code=HTTPStatus.OK)
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
@app.post('/add_appointment', status_code=HTTPStatus.CREATED)   
async def add_appointment(appointment_data: AppointmentCreateModel): 
    new_appointment = Appointment(
        physician_id = appointment_data.physician_id,
        start_date_time = appointment_data.start_date_time,
    )

    appointment = await crud_appointment.create(new_appointment, session)
    return appointment

@app.post('get_appointments/{physician_id}', status_code=HTTPStatus.OK)
async def get_appointments(physician_id: str):
    appointments = await crud_appointment.get_all(session, filter = {"physician_id": physician_id})
    return appointments

@app.post('/edit_appointment/{appointment_id}', status_code=HTTPStatus.OK)
async def edit_appointment(appointment_id: str, appointment_data: AppointmentCreateModel):
    updated_appointment = await crud_appointment.update(appointment_id, appointment_data.dict(exclude_unset=True), session)
    return updated_appointment

@app.post('/delete_appointment/{appointment_id}', status_code=HTTPStatus.OK)
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

'''
    done: create_user(user_id, email)
    done: (implemented in a separate registration) add_patient_detail(user_id, first_name, last_name, age, sex, weight, height, blood_type)
    done: (implemented in a separate registration) add_physician_detail(user_id, first_name, last_name, age, sex, specialization_id)
    done: edit_physician(user_id, first_name, last_name, age, sex, specialization_id, type)
    done: edit_patient(user_id, first_name, last_name, age, sex, weight, height, blood_type)
    delete_user(user_id)
    get_specializations()
    get_appointments(physician_id) // returns all available appointments for that specialization
    add_appointment(date_time, phsyician_id, duration)
    edit_appointment(appointment_id, date_time, duration)
    delete_appointment(appointment_id)
    book_appointment(appointment_id)
    generate_document(audio_blob)
'''