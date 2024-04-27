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

# here use the CRUD class to interact with the database
db = CRUD()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post('/register', status_code=HTTPStatus.CREATED)
async def create_user(user_data: UserCreateModel, 
                      patient_data: PatientCreateModel = None, 
                      physician_data: PhysicianCreateModel = None, 
                      user_type: str = Query(..., description="Type parameter")):
    new_user = User(
        user_id = user_data.user_id,
        first_name = user_data.first_name,
        last_name = user_data.last_name,
        email = user_data.email,
        phone_number = user_data.phone_number,
    )

    user = await db.create_user(new_user, session)

    if user_type == 'patient':
        if not patient_data:
            raise HTTPException(status_code=400, detail="Missing patient data")
        new_patient = Patient(
            patient_data.user_id,
            patient_data.height,
            patient_data.weight,
        )
        patient = await db.create_patient(new_patient, session)
        return {"user": user, "patient": patient}
        # return user, patient

    elif user_type == 'physician':
        if not physician_data:
            raise HTTPException(status_code=400, detail="Missing physician data")
        new_physician = Physician(
            physician_data.user_id,
            physician_data.height,
            physician_data.weight,
        )
        physician = await db.create_physician(new_physician, session)
        return {"user": user, "physician": physician}

    else:
        raise HTTPException(status_code=400, detail="Invalid user type")
        # return user, physician # or patient or physician