"""
Database related utilities
"""

from database_and_models import SessionLocal


def get_db():
    """
    Returns a db session connection
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
