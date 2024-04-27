# This file will act as the entry point for your application. It will initialize
# the app and database connections, define routes, and include any configuration
# settings.

# standard library
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
from schemas import UserCreateModel


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


@app.post('/register/{user_type}', status_code=HTTPStatus.CREATED)
async def create_user(user_data: UserCreateModel, user_type: str = Query(None, description="Type parameter")):
    new_user = User(
        user_id = user_data.user_id,
        first_name = user_data.first_name,
        last_name = user_data.last_name,
        email = user_data.email,
        phone_number = user_data.phone_number,
    )

    if user_type == 'patient':
        new_patient = Pa

    user = await db.create_user(new_user, session)

    return user