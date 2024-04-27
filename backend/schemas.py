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
    phone_number: str

    model_config = ConfigDict(
        from_attributes=True,
        # orm_mode=True
    )

class UserCreateModel(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    email: str
    phone_number: str

    model_config = ConfigDict(
        from_attributes=True,
        # orm_mode=True,
        # shows up as the example in the swagger docs for Create Article
        json_schema_extra={
            "example": {
                "user_id": "0",
                "first_name": "The first name of the user",
                "last_name": "The last name of the user",
                "email": "The email of the user",
                "phone_number": "The phone number of the user",
            }
        }
    )

# ----- Models for Patient ----- #
class PatientModel(BaseModel):
    user_id: str
    height: str
    weight: str

    model_config = ConfigDict(
        from_attributes=True,
        # orm_mode=True
    )

class PatientCreateModel(BaseModel):
    # user_id: str
    height: str
    weight: str

    model_config = ConfigDict(
        from_attributes=True,
        # orm_mode=True,
        # shows up as the example in the swagger docs for Create Article
        json_schema_extra={
            "example": {
                "height": "The height of the patient",
                "weight": "The weight of the patient",
            }
        }
    )

# ----- Models for Physician ----- #
class PhysicianModel(BaseModel):
    user_id: str
    specialization_id: int

    model_config = ConfigDict(
        from_attributes=True,
        # orm_mode=True
    )

class PhysicianCreateModel(BaseModel):
    # user_id: str
    specialization_id: int

    model_config = ConfigDict(
        from_attributes=True,
        # orm_mode=True,
        # shows up as the example in the swagger docs for Create Article
        json_schema_extra={
            "example": {
                "specialization_id": "0",
            }
        }
    )