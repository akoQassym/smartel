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
            appointment_id = "457d2963-2f8c-4551-bacd-ca9d7a2b954a"
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