"""
Utilities related to address
"""
from sqlalchemy.orm import Session
import database_and_models
import schemas


def create_address(
    db: Session,
    address: schemas.AddressCreate
) -> schemas.Address:
    """
    Stores the given address in the database
    """
    address_record = database_and_models.Address(**address.model_dump())
    db.add(address_record)
    db.commit()
    db.refresh(address_record)
    return address_record


def get_address(
    db: Session,
    address_id: int
) -> schemas.Address:
    """
    Returns saved address from the db against the given id
    """
    saved_address_record = db.query(database_and_models.Address)\
        .filter(database_and_models.Address.id == address_id).first()
    return saved_address_record
