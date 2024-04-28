# Define your database models here. This keeps your database schema separate
# from your business logic, which is generally a good practice.
# You basically define your tables here

from base import Base, engine
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    user_id : Mapped[str] = mapped_column(primary_key = True)
    first_name : Mapped[str] = mapped_column(nullable=False)
    last_name : Mapped[str] = mapped_column(nullable=False)
    email : Mapped[str] = mapped_column(nullable=False)

class Patient(Base):
    __tablename__ = 'patients'

    user_id: Mapped[str] = mapped_column(ForeignKey('users.user_id'), primary_key=True)
    height: Mapped[str] = mapped_column(nullable=False)
    weight: Mapped[str] = mapped_column(nullable=False)
    phone_number : Mapped[str] = mapped_column(nullable=False)
    birth_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    sex: Mapped[str] = mapped_column(nullable=False)
    blood_type: Mapped[str] = mapped_column(nullable=False)
    #__mapper_args__ = {'polymorphic_identity': 'patient'}

class Physician(Base):
    __tablename__ = 'physicians'

    user_id: Mapped[str] = mapped_column(ForeignKey('users.user_id'), primary_key=True)
    specialization_id: Mapped[int] = mapped_column(ForeignKey('specializations.specialization_id'))
    phone_number : Mapped[str] = mapped_column(nullable=False)
    birth_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    sex: Mapped[str] = mapped_column(nullable=False)

    specialization: Mapped['Specialization'] = relationship('Specialization', back_populates='physicians')
    appointments: Mapped['Appointment'] = relationship('Appointment', back_populates='physician')
    #__mapper_args__ = {'polymorphic_identity': 'physician'}

    # This function tells SQLAlchemy how two tables are related to each other,
    # which is essential for generating SQL for queries that span multiple
    # tables without having to manually write the joins.

class Specialization(Base):
    __tablename__ = 'specializations'

    specialization_id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    physicians: Mapped['Physician'] = relationship('Physician', back_populates='specialization')

class Appointment(Base):
    __tablename__ = 'appointments'

    appointment_id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    start_date_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    isBooked: Mapped[bool] = mapped_column(nullable=False, default=False)

    physician_id: Mapped[str] = mapped_column(ForeignKey('physicians.user_id'), nullable=False)
    patient_id: Mapped[str] = mapped_column(ForeignKey('patients.user_id'), nullable=True)

    physician: Mapped['Physician'] = relationship('Physician', back_populates='appointments')
    patient: Mapped['Patient'] = relationship('Patient')

class SummaryDocument(Base):
    __tablename__ = 'summary_documents'

    summary_doc_id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    appointment_id: Mapped[str] = mapped_column(ForeignKey('appointments.appointment_id'))
    transcription: Mapped[str] = mapped_column(Text, nullable=True, default=None)
    markdown_summary: Mapped[str] = mapped_column(Text, nullable=True, default=None)

    appointment: Mapped['Appointment'] = relationship('Appointment')