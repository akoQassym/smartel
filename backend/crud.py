# Contains functions for creating, reading, updating, and deleting data (CRUD)
# operations and any other business logic into this file. This centralizes the
# logic for interacting with the database models, making it easier to manage.

# import libraries
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select

# import functions
from models import User #, Patient, Physician, Specialization, Appointments, SummaryDocument

class CRUD:
    async def create_user(self, user_id: int, async_session: async_sessionmaker[AsyncSession]):
        pass 
        # async with async_sessionmaker() as session:
        #     user = User(user_id = user_id)
        #     session.add(user)
        #     await session.commit()
        #     return user