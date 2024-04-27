# Define your database models here. This keeps your database schema separate
# from your business logic, which is generally a good practice.

from base import Base, engine
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, ForeignKey, DateTime
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    user_id : Mapped[int] = mapped_column(primary_key = True)
    first_name : Mapped[str] = mapped_column(nullable=False)
    last_name : Mapped[str] = mapped_column(nullable=False)
    email : Mapped[str] = mapped_column(nullable=False)
    phone_number : Mapped[str] = mapped_column(nullable=False)

class Patient(User):
    __tablename__ = 'patients'
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'), primary_key=True)
    height: Mapped[str] = mapped_column(nullable=False)
    weight: Mapped[str] = mapped_column(nullable=False)
    #__mapper_args__ = {'polymorphic_identity': 'patient'}

class Physician(User):
    __tablename__ = 'physicians'
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'), primary_key=True)
    specialization_id: Mapped[int] = mapped_column(ForeignKey('specializations.specialization_id'))

    specialization: Mapped['Specialization'] = relationship('Specialization', back_populates='physicians')
    appointments: Mapped['Appointment'] = relationship('Appointment', back_populates='physician')
    #__mapper_args__ = {'polymorphic_identity': 'physician'}

class Specialization(Base):
    __tablename__ = 'specializations'
    specialization_id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    physicians: Mapped['Physician'] = relationship('Physician', back_populates='specialization')

class Appointment(Base):
    __tablename__ = 'appointments'
    appointment_id: Mapped[int] = mapped_column(primary_key=True)
    date_time: Mapped[datetime] = mapped_column(nullable=False)
    isBooked: Mapped[bool] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(Text)

    physician_id: Mapped[int] = mapped_column(ForeignKey('physicians.user_id'))
    patient_id: Mapped[int] = mapped_column(ForeignKey('patients.user_id'))

    physician: Mapped['Physician'] = relationship('Physician', back_populates='appointments')
    patient: Mapped['Patient'] = relationship('Patient')

class SummaryDocument(Base):
    __tablename__ = 'summary_documents'
    summaryDocId: Mapped[int] = mapped_column(primary_key=True)
    appointment_id: Mapped[int] = mapped_column(ForeignKey('appointments.appointment_id'))

    appointment: Mapped['Appointment'] = relationship('Appointment')