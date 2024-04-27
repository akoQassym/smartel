# Contains functions for creating, reading, updating, and deleting data (CRUD)
# operations and any other business logic into this file. This centralizes the
# logic for interacting with the database models, making it easier to manage.

# import libraries
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

# import functions
from models import User, Patient, Physician #, Specialization, Appointments, SummaryDocument


class CRUD:
    # ----- CRUD for User ----- #
    async def create_user(self, user: User, async_session: async_sessionmaker[AsyncSession]):
        async with async_session() as session:
            session.add(user)
            await session.commit()
            await session.refresh(user) # refresh the user object to get the updated user object
            return user

    async def get_user(self, user_id: int, async_session: async_sessionmaker[AsyncSession]):
        async with async_session() as session:
            query = select(User).filter(User.user_id == user_id)
            result = await session.execute(query)
            try:
                return result.scalar().one()
            except NoResultFound:
                return None

    async def get_all_users(self, async_session: async_sessionmaker[AsyncSession]):
        async with async_session() as session:
            query = select(User)
            result = await session.execute(query)
            return result.scalars().all()

    async def update_user(self, user_id: int, update_data: dict, async_session: async_sessionmaker[AsyncSession]):
        async with async_session() as session:
            query = select(User).filter(User.user_id == user_id)
            result = await session.execute(query)
            try:
                user = result.scalar().one()
                for key, value in update_data.items():
                    setattr(user, key, value)
                await session.commit()
                return user
            except NoResultFound:
                return None

    async def delete_user(self, user_id: int, async_session: async_sessionmaker[AsyncSession]):
        async with async_session() as session:
            query = select(User).filter(User.user_id == user_id)
            result = await session.execute(query)
            try:
                user = result.scalar().one()
                session.delete(user)
                await session.commit()
                return True
            except NoResultFound:
                return False

    # ----- CRUD for Patients ----- #
    async def create_patient(self, patient: Patient, async_session: async_sessionmaker[AsyncSession]):
        async with async_session() as session:
            session.add(patient)
            await session.commit()
            await session.refresh(patient)
            return patient

    async def get_patient(self, patient_id: int, async_session: async_sessionmaker[AsyncSession]):
        async with async_session() as session:
            query = select(Patient).filter(Patient.user_id == patient_id)
            result = await session.execute(query)
            try:
                return result.scalar().one()
            except NoResultFound:
                return None

    async def get_all_patients(self, async_session: async_sessionmaker[AsyncSession]):
        async with async_session() as session:
            query = select(Patient)
            result = await session.execute(query)
            return result.scalars().all()

    async def update_patient(self, patient_id: int, update_data: dict, async_session: async_sessionmaker[AsyncSession]):
        async with async_session() as session:
            query = select(Patient).filter(Patient.user_id == patient_id)
            result = await session.execute(query)
            try:
                patient = result.scalar().one()
                for key, value in update_data.items():
                    setattr(patient, key, value)
                await session.commit()
                return patient
            except NoResultFound:
                return None

    async def delete_patient(self, patient_id: int, async_session: async_sessionmaker[AsyncSession]):
        async with async_session() as session:
            query = select(Patient).filter(Patient.user_id == patient_id)
            result = await session.execute(query)
            try:
                patient = result.scalar().one()
                session.delete(patient)
                await session.commit()
                return True
            except NoResultFound:
                return False

    # ----- CRUD for Physician ----- #
    async def create_physician(self, physician: Physician, async_session: async_sessionmaker[AsyncSession]):
        async with async_session() as session:
            session.add(physician)
            await session.commit()
            await session.refresh(physician)
            return physician

    async def get_physician(self, physician_id: int, async_session: async_sessionmaker[AsyncSession]):
        async with async_session() as session:
            query = select(Physician).filter(Physician.user_id == physician_id)
            result = await session.execute(query)
            try:
                return result.scalar().one()
            except NoResultFound:
                return None

    async def get_all_physicians(self, async_session: async_sessionmaker[AsyncSession]):
        async with async_session() as session:
            query = select(Physician)
            result = await session.execute(query)
            return result.scalars().all()

    async def update_physician(self, physician_id: int, update_data: dict, async_session: async_sessionmaker[AsyncSession]):
        async with async_session() as session:
            query = select(Physician).filter(Physician.user_id == physician_id)
            result = await session.execute(query)
            try:
                physician = result.scalar().one()
                for key, value in update_data.items(): 
                # a faster way to update the physician object rather then
                # updating each field individually
                    setattr(physician, key, value)
                await session.commit()
                return physician
            except NoResultFound:
                return None

    async def delete_physician(self, physician_id: int, async_session: async_sessionmaker[AsyncSession]):
        async with async_session() as session:
            query = select(Physician).filter(Physician.user_id == physician_id)
            result = await session.execute(query)
            try:
                physician = result.scalar().one()
                session.delete(physician)
                await session.commit()
                return True
            except NoResultFound:
                return False
