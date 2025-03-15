from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://famagustadb_owner:npg_zeMv72jOIgSy@ep-muddy-brook-abntf4h4-pooler.eu-west-2.aws.neon.tech/famagusa_db?sslmode=require"

# Create Database Engine
engine = create_engine(DATABASE_URL)

# Create Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
