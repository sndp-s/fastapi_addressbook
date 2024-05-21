"""
Address Book API

Author: Sandeep Sharma
Author Email: sandeeptech8@gmail.com

This file contains the main components of the FastAPI application for the Address Book API:

app (FastAPI): Main application instance.
APIs (functions): Endpoint definitions for CRUD operations on addresses.
exception_handlers (functions): Centralized error handlers for API requests.
"""
from fastapi import FastAPI, Depends, status, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
import db_utils
import address_utils
import response_utils
import schemas
from logger import logger

app = FastAPI()


@app.post("/address/")
def create_address(address: schemas.AddressCreate, db: Session = Depends(db_utils.get_db)):
    """
    Endpoint to create new address
    """
    logger.info('Received request to create address: %s', address)
    saved_address = address_utils.create_address(db, address)
    logger.info('Address created successfully: %s', saved_address)

    return response_utils.create_response(
        status_code=status.HTTP_201_CREATED,
        data=schemas.Address.model_validate(saved_address).model_dump(),
        message="Address created successfully!"
    )


@app.get("/address/{address_id}")
def view_address(address_id: int, db: Session = Depends(db_utils.get_db)):
    """
    Returns the address mapped to the given id
    """
    logger.info('Received request to view address with ID: %s', address_id)
    saved_requested_address = address_utils.get_address(db, address_id)
    logger.info('Address retrieved successfully: %s', saved_requested_address)

    return response_utils.create_response(
        status_code=status.HTTP_200_OK,
        message="Address found!",
        data=schemas.Address.model_validate(
            saved_requested_address).model_dump()
    )


@app.put("/address/{address_id}")
def update_address(
    address_id: int,
    address_update: schemas.AddressUpdate,
    db: Session = Depends(db_utils.get_db)
):
    """
    Updates the given fields for the given address_id
    """
    logger.info('Received request to update address with ID: %s', address_id)
    updated_address = address_utils.update_address(
        db, address_id, address_update)
    logger.info('Address updated successfully: %s', updated_address)

    return response_utils.create_response(
        message="Address updated successfully!",
        status_code=status.HTTP_200_OK,
        data=schemas.Address.model_validate(updated_address).model_dump()
    )


@app.delete("/address/{address_id}")
def delete_address(
    address_id: int,
    db: Session = Depends(db_utils.get_db)
):
    """
    Removes the address with given address_id 
    """
    logger.info('Received request to delete address with ID: %s', address_id)
    address_utils.delete_address(db=db, address_id=address_id)
    logger.info('Address with ID %s deleted successfully', address_id)

    return response_utils.create_response(
        status_code=status.HTTP_200_OK,
        message="Address deleted successfully!"
    )


@app.get("/address/within-distance/")
def get_addresses_within_distance(
    distance: float,
    latitude: schemas.Latitude,
    longitude: schemas.Longitude,
    db: Session = Depends(db_utils.get_db)
):
    """
    Returns a list of address with the distance range of given coordinates
    """
    logger.info('Received request to get addresses within %s KM of (lat: %s, long: %s)',
                distance, latitude, longitude)
    addresses = address_utils.get_addresses_within(
        db, distance, latitude, longitude)
    logger.info('Addresses within distance retrieved successfully')

    return response_utils.create_response(
        data={'addresses': [schemas.Address.model_validate(address).model_dump()
              for address in addresses]}
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Central exception handler

    Intercepts all the "HTTPException"s raised in the APIs,
    prepares the response object with appropriate status code and data
    """
    logger.error('HTTPException: %s - %s', exc.status_code, exc.detail)
    return response_utils.create_error_response(
        status_code=exc.status_code,
        message=str(exc.detail)
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Validation exception handler.

    Intercepts all "RequestValidationError"s raised in the APIs due to validation errors,
    prepares the response object with a 422 status code and detailed error messages.
    """
    logger.error('RequestValidationError: %s', exc.errors())
    errors = [schemas.ErrorDetail(
        loc=err["loc"], msg=err["msg"], type=err["type"]).model_dump() for err in exc.errors()]
    return response_utils.create_error_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message="Validation Error",
        errors=errors
    )


@app.exception_handler(Exception)
async def unexpected_exceptions_handler(request: Request, exc: Exception):
    """
    Unexpected exceptions handler - returns response in the standard response structure
    """
    logger.exception('Unexpected exception: %s', exc)
    return response_utils.create_error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message="An unexpected error occurred"
    )
