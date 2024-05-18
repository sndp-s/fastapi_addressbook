"""
Main app - starting point of the application

All the APIs are located here as well
"""

from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
import db_utils
import address_utils
import response_utils
import schemas


app = FastAPI()


@app.get("/")
def hello_world():
    """
    hello world example handler
    """
    return "Hello world!"


@app.post("/address/")
def create_address(address: schemas.AddressCreate, db: Session = Depends(db_utils.get_db)):
    """
    Endpoint to create new address
    """
    saved_address = address_utils.create_address(db, address)

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
    saved_requested_address = address_utils.get_address(db, address_id)
    if not saved_requested_address:
        return response_utils.create_error_response(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Address not found"
        )
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
    updated_address = address_utils.update_address(db, address_id, address_update)

    if not update_address:
        return response_utils.create_error_response(
            message="Address not found!",
            status_code=status.HTTP_400_BAD_REQUEST
        )

    return response_utils.create_response(
        message="Address updated successfully!",
        status_code=status.HTTP_200_OK,
        data=schemas.Address.model_validate(updated_address).model_dump()
    )