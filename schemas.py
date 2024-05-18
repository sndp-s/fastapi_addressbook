"""
Schemas of the models used in the application
"""
from pydantic import BaseModel, ConfigDict

class AddressBase(BaseModel):
    """
    Base model of Address entity
    """
    name: str
    street: str
    city: str
    state: str
    country: str
    latitude: float
    longitude: float

class AddressCreate(AddressBase):
    """
    Schema for Address creation api request body
    """

class Address(AddressBase):
    """
    Address as represented in the Database
    """
    model_config = ConfigDict(from_attributes=True)

    id: int
