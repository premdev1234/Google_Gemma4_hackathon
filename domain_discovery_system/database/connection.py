# domain_discovery_system/database/connection.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
from dotenv import load_dotenv
import os

# ---------------------------------------------------
# LOAD ENV VARIABLES
# ---------------------------------------------------

load_dotenv()

# ---------------------------------------------------
# DATABASE URL
# ---------------------------------------------------

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:password@localhost:5432/domain_discovery_db"
)

# ---------------------------------------------------
# SQLALCHEMY ENGINE
# ---------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    # SQLAlchemy 2.0 mode
    future=True,
    # Debugging
    echo=os.getenv("DB_ECHO", "False") == "True",
    # Connection pooling
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
)

# ---------------------------------------------------
# SESSION FACTORY
# ---------------------------------------------------

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, expire_on_commit=False, bind=engine
)

# ---------------------------------------------------
# BASE MODEL
# ---------------------------------------------------

Base = declarative_base()

# ---------------------------------------------------
# DATABASE SESSION DEPENDENCY
# ---------------------------------------------------


def get_db():
    """
    Creates a new database session
    for every API request.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
