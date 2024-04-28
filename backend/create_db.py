from base import Base, engine
import asyncio

async def recreate_table(table):
    async with engine.begin() as conn:
        # Drop the specified table
        await conn.run_sync(table.__table__.drop, checkfirst=True)
        # Recreate the specified table
        await conn.run_sync(table.__table__.create)

async def create_db():
    # Import here to avoid circular imports
    from models import User, Patient, Physician, Specialization, Appointment, SummaryDocument

    # Recreate only the User table
    await recreate_table(SummaryDocument)

    # Dispose of the engine
    await engine.dispose()

# Run the create_db coroutine to perform the operation
asyncio.run(create_db())
