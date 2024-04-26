# Define your database models here. This keeps your database schema separate
# from your business logic, which is generally a good practice.
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import EmailType, PasswordType

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(EmailType, unique=True, nullable=False)
    password = Column(PasswordType(schemes=['pbkdf2_sha512']), nullable=False)
    role = Column(String(50), nullable=False)
    
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': role
    }

class Doctor(User):
    __mapper_args__ = {
        'polymorphic_identity': 'doctor',
    }
    # Additional Doctor-specific attributes here

class Patient(User):
    __mapper_args__ = {
        'polymorphic_identity': 'patient',
    }
    # Additional Patient-specific attributes here

# Setup your database connection and engine here
engine = create_engine('postgresql://username:password@localhost/mydatabase')
Base.metadata.create_all(engine)
