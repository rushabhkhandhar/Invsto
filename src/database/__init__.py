import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Direct database URL instead of importing from config to avoid circular imports
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/trading_db")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

def initialize_db():
    """Initialize the database by creating all tables"""
    from .models import StockData  # Import here to avoid circular imports
    Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency for getting DB session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()