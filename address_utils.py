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
from logger import logger


def create_address(
    db: Session,
    address: schemas.AddressCreate
) -> schemas.Address:
    """
    Stores the given address in the database
    """
    logger.info('Creating new address: %s', address)
    try:
        address_record = database_and_models.Address(
            **address.model_dump())
        db.add(address_record)
        db.commit()
        db.refresh(address_record)
        logger.info('New address created successfully: %s', address_record)
        return address_record
    except IntegrityError as exc:
        logger.error('Integrity error while creating new address: %s', exc)
        # Handle unique constraint violation
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Address with the same name already exists."
        ) from exc
    except SQLAlchemyError as exc:
        logger.error('SQLAlchemy error while creating new address: %s', exc)
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
    try:
        logger.info('Retrieving address with ID: %s', address_id)
        saved_address_record = db.query(database_and_models.Address)\
            .filter(database_and_models.Address.id == address_id).first()

        if not saved_address_record:
            logger.error('Address with ID: %s not found', address_id)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address not found"
            )

        logger.info('Address with ID: %s retrieved successfully', address_id)
        return saved_address_record
    except SQLAlchemyError as exc:
        logger.exception(
            'An unexpected database error occurred while retrieving address with ID: %s', address_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while retrieving the address."
        ) from exc


def update_address(
    db: Session,
    address_id: int,
    address_update: schemas.AddressUpdate
) -> schemas.Address:
    """
    Updates the given fields of the address belonging to the given address id
    """
    logger.info('Updating address with ID: %s', address_id)
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
                logger.warning(
                    'Address with ID: %s does not exist in the system', address_id)
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No address found with ID: {address_id}"
                )

            logger.info('Address with ID: %s updated successfully', address_id)

        # Retrieve the updated address after the transaction is committed
        updated_address = db.query(database_and_models.Address)\
            .filter(database_and_models.Address.id == address_id).first()

        return updated_address

    except IntegrityError as exc:
        logger.error(
            'Integrity error while updating address with ID: %s', address_id)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot update address: Data integrity issue"
        ) from exc
    except SQLAlchemyError as exc:
        logger.exception(
            'An unexpected database error occurred while updating address with ID: %s', address_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while updating the address."
        ) from exc


def delete_address(db: Session, address_id: int) -> None:
    """
    Deletes the address corresponding to the given address_id
    """
    logger.info('Attempting to delete address with ID: %s', address_id)
    try:
        # Check if the address exists before attempting to delete it
        db_address = get_address(db, address_id)

        # Delete the address if it exists
        db.delete(db_address)
        db.commit()

        logger.info('Address with ID: %s deleted successfully', address_id)

    except HTTPException as exc:
        if exc.status_code == status.HTTP_404_NOT_FOUND:
            logger.warning('Address with ID: %s does not exist', address_id)
        raise
    except SQLAlchemyError as exc:
        logger.exception(
            'An unexpected database error occurred while deleting address with ID: %s', address_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while deleting the address."
        ) from exc


def get_nearby_addresses(
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
    logger.info(
        'Locating Addresses within %s KMs of (lat, long): (%s, %s)',
        distance, latitude, longitude
    )

    try:
        user_location = (latitude, longitude)
        addresses_within_distance = []
        all_addresses = db.query(database_and_models.Address).all()
        for address in all_addresses:
            address_location = (address.latitude, address.longitude)
            if geo_distance(user_location, address_location).km <= distance:
                addresses_within_distance.append(address)

        logger.info(
            'Found %s addresses within %s KMs of (lat, long): (%s, %s)',
            len(addresses_within_distance), distance, latitude, longitude
        )
        return addresses_within_distance

    except SQLAlchemyError as exc:
        logger.exception(
            'An unexpected database error occurred while locating addresses within %s KMs of (lat, long): (%s, %s)',
            distance, latitude, longitude
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while locating the addresses."
        ) from exc


def get_all_addresses(
    db: Session,
) -> Union[List[schemas.Address], List]:
    """
    Returns all of the saved addresses from the db
    """
    try:
        logger.info('Retrieving all addresses int the db')
        all_saved_address_records = db.query(database_and_models.Address).all()
        logger.info('All addresses retrieved successfully')
        return all_saved_address_records
    except SQLAlchemyError as exc:
        logger.exception(
            'An unexpected database error occurred while retrieving all addresses')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while retrieving all addresses."
        ) from exc
