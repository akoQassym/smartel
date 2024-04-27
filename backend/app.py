# This file will act as the entry point for your application. It will initialize
# the app and database connections, define routes, and include any configuration
# settings.

# standard library
from http.client import HTTPException
from fastapi import FastAPI, Query, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from http import HTTPStatus
from fastapi.middleware.cors import CORSMiddleware
# from pandas import pd
from typing import List
import uuid

# local library
from crud import CRUD
from base import engine
from models import User, Patient, Physician, Specialization, Appointment, SummaryDocument
from schemas import UserCreateModel, PatientCreateModel, PhysicianCreateModel #, SpecializationCreateModel, AppointmentCreateModel, SummaryDocumentCreateModel


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


@app.post('/register', status_code=HTTPStatus.CREATED)
async def create_user(user_data: UserCreateModel): 
    new_user = User(
        user_id = user_data.user_id,
        first_name = user_data.first_name,
        last_name = user_data.last_name,
        email = user_data.email,
        # phone_number = user_data.phone_number,
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

'''
create_user(user_id, email)
add_patient_detail(user_id, first_name, last_name, age, sex, weight, height, blood_type)
add_physician_detail(user_id, first_name, last_name, age, sex, specialization_id)
edit_physician(user_id, first_name, last_name, age, sex, specialization_id, type)
edit_patient(user_id, first_name, last_name, age, sex, weight, height, blood_type)
delete_user(user_id)
get_specializations()
get_appointments(physician_id) // returns all available appointments for that specialization
add_appointment(date_time, phsyician_id, duration)
edit_appointment(appointment_id, date_time, duration)
delete_appointment(appointment_id)
book_appointment(appointment_id)
generate_document(audio_blob)
'''