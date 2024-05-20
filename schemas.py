"""
Schemas of the models used in the application
"""
from typing import Optional, List, Union
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


class AddressUpdate(AddressBase):
    """
    Schema for Address updation api request body
    """
    name: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class Address(AddressBase):
    """
    Address as represented in the Database
    """
    model_config = ConfigDict(from_attributes=True)

    id: int
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None


class ErrorDetail(BaseModel):
    """
    Represents each error object in the errors list
    """
    loc: Union[List[str], List[int]]
    msg: str
    type: str
