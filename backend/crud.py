# Contains functions for creating, reading, updating, and deleting data (CRUD)
# operations and any other business logic into this file. This centralizes the
# logic for interacting with the database models, making it easier to manage.

# import libraries
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

# import functions
from models import User, Patient, Physician, Specialization, Appointment, SummaryDocument

class CRUD:
    def __init__(self, model):
        self.model = model
        self.model_name = model.__name__.lower()

    async def create(self, instance_data, async_session: async_sessionmaker[AsyncSession]):
        async with async_session() as session:
            session.add(instance_data)
            await session.commit()
            await session.refresh(instance_data)
            return instance_data

    async def get_one(self, id, async_session: async_sessionmaker[AsyncSession]):
        async with async_session() as session:
            query = select(self.model).filter_by(user_id=id)
            result = await session.execute(query)
            try:
                return result.scalar_one()
            except NoResultFound:
                return None

    async def get_all(self, async_session: async_sessionmaker[AsyncSession]):
        async with async_session() as session:
            query = select(self.model)
            result = await session.execute(query)
            return result.scalars().all()

    async def update(self, id, update_data, async_session: async_sessionmaker[AsyncSession]):
        async with async_session() as session:
            query = select(self.model).filter_by(id=id)
            result = await session.execute(query)
            try:
                instance = result.scalar_one()
                for key, value in update_data.items():
                    setattr(instance, key, value)
                await session.commit()
                
                return instance
            except NoResultFound:
                return None

    async def delete(self, id, async_session: async_sessionmaker[AsyncSession]):
        async with async_session() as session:
            query = select(self.model).filter_by(id=id)
            result = await session.execute(query)
            try:
                instance = result.scalar_one()
                session.delete(instance)
                await session.commit()
                return True
            except NoResultFound:
                return False

'''
Use case:
    crud_user = CRUD(User)
    crud_patient = CRUD(Patient)
    crud_physician = CRUD(Physician)
    crud_specialization = CRUD(Specialization)
    crud_appointment = CRUD(Appointment)
    crud_summary_document = CRUD(SummaryDocument)
'''


