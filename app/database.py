from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from sqlalchemy.orm import Session

# Database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # SQLite for testing purposes

# Creating an engine to interact with the database
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session local for dependency injection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declare the base class for ORM models
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
