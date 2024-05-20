"""
Utilities related to address
"""
from typing import List, Union
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
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
    try:
        with db.begin():
            address_record = database_and_models.Address(
                **address.model_dump())
            db.add(address_record)
            db.commit()
            db.refresh(address_record)
        return address_record
    except IntegrityError as exc:
        # Handle unique constraint violation
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Address with the same name already exists."
        ) from exc
    except SQLAlchemyError as exc:
        # Handle other database errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while storing the address."
        ) from exc


def get_address(
    db: Session,
    address_id: int
) -> schemas.Address:
    """
    Returns saved address from the db against the given id
    """
    saved_address_record = db.query(database_and_models.Address)\
        .filter(database_and_models.Address.id == address_id).first()
    if not saved_address_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found"
        )
    return saved_address_record


def update_address(
    db: Session,
    address_id: int,
    address_update: schemas.AddressUpdate
) -> schemas.Address:
    """
    Updates the given fields of the address belonging to the given address id
    """
    try:
        # Extract non-empty fields from the update payload
        fields_to_update = {k: v for k,
                            v in address_update.model_dump().items() if v}

        # Perform the update operation within a context manager
        with db.begin():
            # Update the address record
            num_updated = db.query(database_and_models.Address)\
                .filter(database_and_models.Address.id == address_id)\
                .update(fields_to_update)

            # If no record was updated, raise an HTTPException
            if num_updated == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No address found with ID: {address_id}"
                )

        # Retrieve the updated address after the transaction is committed
        updated_address = db.query(database_and_models.Address)\
            .filter(database_and_models.Address.id == address_id).first()

        return updated_address

    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot update address: Bad update data"
        ) from exc


def delete_address(db: Session, address_id: int) -> None:
    """
    Deletes the address corresponding to the given address_id
    """
    # Check if the address exists before attempting to delete it
    db_address = get_address(db, address_id)
    if not db_address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Address with ID {address_id} not found"
        )

    # Delete the address if it exists
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
