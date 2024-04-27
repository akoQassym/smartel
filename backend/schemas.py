# Keep this file to define serialization and deserialization schemas. This helps
# in validating and structuring the input and output data for your API
# endpoints.

from pydantic import BaseModel, ConfigDict
from datetime import datetime

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
                "user_id": "The user id of the user; here it should be a Clerk_id",
                "first_name": "The first name of the user",
                "last_name": "The last name of the user",
                "email": "The email of the user",
                "phone_number": "The phone number of the user",
            }
        }
    )