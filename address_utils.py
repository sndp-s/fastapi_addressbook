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
