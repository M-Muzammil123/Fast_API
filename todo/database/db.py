import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Load environmental variables
load_dotenv()

DATABASE_URL = os.getenv("Database_URL")

if not DATABASE_URL:
    raise ValueError("Database_URL environment variable is not set in the environment or .env file.")

# Initialize the SQLAlchemy engine
# Neon PostgreSQL database URL starts with postgresql:// and needs SSL parameters if not already in URL
engine = create_engine(DATABASE_URL)

# Configure the session factory
SessionLocal = sessionmaker(autocommit=False, 
                            autoflush=False, 
                            bind=engine
                            )

def get_db():
    """
    FastAPI dependency that provides a transactional database session.
    Ensures that the session is closed after the request is processed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
