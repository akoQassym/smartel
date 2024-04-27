# Define your database models here. This keeps your database schema separate
# from your business logic, which is generally a good practice.
# You basically define your tables here

from base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    user_id : Mapped[int] = mapped_column(primary_key = True)
    first_name : Mapped[str] = mapped_column()
    last_name : Mapped[str] = mapped_column()
    email : Mapped[str] = mapped_column()
    phone_number : Mapped[str] = mapped_column()
    password : Mapped[str] = mapped_column()

# class Patient(Base):
#     __tablename__ = "patient"
#     pass

# class Physician(Base):
#     __tablename__ = "physician"
#     pass

# class Specialization(Base):
#     __tablename__ = "specialization"
#     pass

# class Appointments(Base):
#     __tablename__ = "appointments"
#     pass

# class SummaryDocument(Base):
#     __tablename__ = "summary_document"
#     pass