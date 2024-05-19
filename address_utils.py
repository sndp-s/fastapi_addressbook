"""
Utilities related to address
"""
from typing import List, Union
from sqlalchemy.orm import Session
from geopy.distance import distance as geo_distance
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


def get_addresses_within(
    db: Session,
    distance: float,
    latitude: float,
    longitude: float
) -> Union[List[schemas.Address], List]:
    """
    Returns a list of Addresses lying within the given distance range of the given coordinates.

    Note:
    The current implementation is a naive one. In a real-world scenario,
    it would be more efficient to first calculate the maximum and minimum
    latitude and longitude bounds for the given distance. Then, we could 
    prepare the query to filter addresses within these bounds, reducing 
    the number of distance calculations needed.
    """
    user_location = (latitude, longitude)
    addresses_within_distance = []
    all_addresses = db.query(database_and_models.Address).all()
    for address in all_addresses:
        address_location = (address.latitude, address.longitude)
        if geo_distance(user_location, address_location).km <= distance:
            addresses_within_distance.append(address)
    return addresses_within_distance
