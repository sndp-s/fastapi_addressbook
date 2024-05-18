"""
Handles creation of database engine and session
Defines models
"""

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings

# Create engine
engine = create_engine(
    url=settings.database_connection_url,
    connect_args={"check_same_thread": False}
)


# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create Base for models
Base = declarative_base()


# Database Models
class Address(Base):
    """
    Al the addresses are stored here
    """

    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    street = Column(String, index=True)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    latitude = Column(Float, nullable=False, index=True)
    longitude = Column(Float, nullable=False, index=True)


# Create database tables
# NOTE In the real world application, I would handle db migration with alembic
# and also keep models and database files separate
# Models have to be declared on the Base object first,
# inorder to create tables in the database in the mext step
Base.metadata.create_all(engine)
