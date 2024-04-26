# This file will act as the entry point for your application. It will initialize
# the app and database connections, define routes, and include any configuration
# settings.

# standard library
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from http import HTTPStatus
# from pandas import pd
from typing import List
import uuid

# local library
from crud import CRUD
from base import engine
from models import User #, Patient, Physician, Specialization, Appointments, SummaryDocument



app = FastAPI(
    title = "Smartel API",
    description = "API for Smartel",
    docs_url = "/",
)

session = async_sessionmaker(
    bind = engine,
    expir_on_commit = False,
)

# here use the CRUD class to interact with the database
db = CRUD()

@app.get("/")
async def root():
    return {"message": "Hello World"}

