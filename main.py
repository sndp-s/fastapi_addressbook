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
def create_address(address: schemas.AddressCreate, db:Session=Depends(db_utils.get_db)):
    """
    Endpoint to create new address
    """
    saved_address = address_utils.create_address(db, address)

    return response_utils.create_response(
        status_code=status.HTTP_201_CREATED,
        data=schemas.Address.model_validate(saved_address).model_dump(),
        message="Address created successfully!"
    )
