# This file will act as the entry point for your application. It will initialize
# the app and database connections, define routes, and include any configuration
# settings.

# standard library
from http.client import HTTPException
from fastapi import FastAPI, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from http import HTTPStatus
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

session = async_sessionmaker(
    bind = engine,
    expire_on_commit = False,
)

# here use the CRUD class to interact with the database initializing class takes
# a good amount of time, so it is preferable to create a global instance to use
# it throughout the application
db = CRUD()

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

    user = await db.create_user(new_user, session)

    return user

@app.post('/register/patient', status_code=HTTPStatus.CREATED)
async def create_physician(patient_data: PatientCreateModel):
    new_patient = Patient(
        height = patient_data.height,
        weight = patient_data.weight
    )

    patient = await db.create_patient(new_patient, session)

    return patient

@app.post('/register/physician', status_code=HTTPStatus.CREATED)
async def create_physician(physician_data: PhysicianCreateModel):
    new_physician = Physician(
        specialization_id = physician_data.specialization_id,
    )

    physician = await db.create_physician(new_physician, session)

    return physician