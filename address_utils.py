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


def update_address(
    db: Session,
    address_id: int,
    address_update: schemas.AddressUpdate
) -> schemas.Address:
    """
    Updates the given fields of the address belonging to the given address id
    """
    fields_to_update = {k: v for k,
                        v in address_update.model_dump().items() if v}
    db.query(database_and_models.Address)\
        .filter(database_and_models.Address.id == address_id).update(fields_to_update)
    db.commit()
    return db.query(database_and_models.Address)\
        .filter(database_and_models.Address.id == address_id).first()


def delete_address(db: Session, address_id: int) -> None:
    """
    Deletes the address corresponding to the given addredd_id
    """
    db_address = get_address(db, address_id)
    if db_address:
        db.delete(db_address)
        db.commit()
