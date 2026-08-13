import uuid

from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, relationship, Session,sessionmaker
import requests

class Base(DeclarativeBase):
    pass


print("Creating engine...")

engine = create_engine("postgresql+psycopg://postgres:admin123@localhost:5432/job_finder")


SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

