# Keep this file to define serialization and deserialization schemas. This helps
# in validating and structuring the input and output data for your API
# endpoints.

from pydantic import BaseModel, ConfigDict
from datetime import datetime

# ----- Models for User ----- #
class UserModel(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    email: str
    # phone_number: str

    model_config = ConfigDict(
        from_attributes=True,
        # orm_mode=True
    )

class UserCreateModel(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    email: str

    model_config = ConfigDict(
        from_attributes=True,
        # orm_mode=True,
        # shows up as the example in the swagger docs for Create Article
        json_schema_extra={
            "example": {
                "user_id": "0",
                "first_name": "The first name of the user",
                "last_name": "The last name of the user",
                "email": "The email of the user"
            }
        }
    )

# ----- Models for Patient ----- #
class PatientModel(BaseModel):
    user_id: str
    height: str
    weight: str
    phone_number: str
    sex: str
    birth_date: datetime
    blood_type: str

    model_config = ConfigDict(
        from_attributes=True,
        orm_mode=True
    )

class PatientCreateModel(BaseModel):
    height: str
    weight: str
    phone_number: str
    sex: str
    birth_date: datetime
    blood_type: str

    model_config = ConfigDict(
        from_attributes=True,
        orm_mode=True,
        json_schema_extra={
            "example": {
                "height": "The height of the patient",
                "weight": "The weight of the patient",
                "phone_number": "The phone number of the user",
                "sex": "Can be male, female, or other",
                "birth_date": "2024-04-12T14:30:00",
                "blood_type": "The blood type of the patient"
            }
        }
    )

# ----- Models for Physician ----- #
class PhysicianModel(BaseModel):
    user_id: str
    specialization_id: str
    phone_number: str
    sex: str
    birth_date: datetime

    model_config = ConfigDict(
        from_attributes=True,
        orm_mode=True
    )

class PhysicianCreateModel(BaseModel):
    specialization_id: str
    phone_number: str
    sex: str
    birth_date: datetime

    model_config = ConfigDict(
        from_attributes=True,
        orm_mode=True,

        json_schema_extra={
            "example": {
                "specialization_id": "0",
                "phone_number": "The phone number of the user",
                "sex": "Can be male, female, or other",
                "birth_date": "2024-04-12T14:30:00"
            }
        }
    )

# ----- Models for Specialization ----- #
class SpecializationModel(BaseModel):
    specialization_id: str
    description: str
    name: str

    class Config:
        orm_mode = True

class SpecializationCreateModel(BaseModel):
    description: str
    name: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Cardiology",
                "description": "The study of the heart and its functions"
            }
        }

# ----- Models for Appointment ----- #
class AppointmentModel(BaseModel):
    appointment_id: str
    start_date_time: datetime
    isBooked: bool
    physician_id: str
    patient_id: str

    class Config:
        orm_mode = True

class AppointmentCreateModel(BaseModel):
    start_date_time: datetime

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "date_time": "2024-04-12T14:30:00",
                "isBooked": True,
                "description": "Quarterly check-up",
                "physician_id": "clerk_id",
                "patient_id": "clerk_id"
            }
        }

# ----- Models for SummaryDocument ----- #
class SummaryDocumentModel(BaseModel):
    summary_doc_id: str
    appointment_id: str
    transcription: str
    markdown_summary: str

    class Config:
        orm_mode = True

class SummaryDocumentCreateModel(BaseModel):
    appointment_id: str
    transcription: str
    markdown_summary: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "appointment_id": "A type uuid string for foreign key reference",
                "transcription": "The transcription of the appointment",
                "markdown_summary": "The markdown summary of the appointment"
            }
        }
