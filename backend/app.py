# This file will act as the entry point for your application. It will initialize
# the app and database connections, define routes, and include any configuration
# settings.

# standard library
from http.client import HTTPException
from fastapi import FastAPI, Query, Body
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from http import HTTPStatus
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


@app.post('/add_spec', status_code=HTTPStatus.CREATED)
async def add_spec(spec_data: SpecializationCreateModel): 
    new_specialization = Specialization(
        description = spec_data.description,
        name = spec_data.name,
    )

    spec = await crud_specialization.create(new_specialization, session)
    return spec

@app.post('/add_appointment/{physician_id}', status_code=HTTPStatus.CREATED)
async def add_appointment(physician_id: str, app_data: AppointmentCreateModel): 
    new_appointment = Appointment(
        physician_id = physician_id,
        start_date_time = app_data.start_date_time,
    )

    app = await crud_appointment.create(new_appointment, session)
    return app

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