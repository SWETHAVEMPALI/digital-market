"""Database connection and session management.

This file creates the SQLAlchemy engine that talks to Postgres,
and provides a SessionLocal class for creating database sessions.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings


# Create the database engine - this is the actual connection to Postgres
# The connect_args is needed for SQLite but harmless for Postgres
engine = create_engine(
    settings.database_url,
    echo=settings.debug,  # When True, prints all SQL queries. Useful for learning
    pool_pre_ping=True,   # Checks connection is alive before using it
)


# SessionLocal is a factory for creating database sessions
# A session is a "conversation" with the database - you use it to query and save
SessionLocal = sessionmaker(
    autocommit=False,    # Don't auto-commit changes - we'll commit manually
    autoflush=False,     # Don't auto-flush - more control
    bind=engine,         # Connect sessions to our engine
)


# Base class for all our models
# Every model we create will inherit from this
Base = declarative_base()


# Dependency function for FastAPI
# This is what we'll use in our endpoints to get a database session
def get_db():
    """Provide a database session to an endpoint, then close it.

    Usage in an endpoint:
        def my_endpoint(db: Session = Depends(get_db)):
            ...

    The `yield` makes this a generator. FastAPI handles the cleanup
    automatically - the session gets closed after the request finishes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()