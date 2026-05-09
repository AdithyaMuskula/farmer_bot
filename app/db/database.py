from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database file (this will be created automatically)
DATABASE_URL = "sqlite:///./farmer.db"

# Create engine (connection)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # needed for SQLite
)

# Session (used to talk to DB)
SessionLocal = sessionmaker(bind=engine)

# Base class (used for creating tables)
Base = declarative_base()