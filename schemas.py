"""
Schemas of the models used in the application
"""
from typing import Optional, List, Union, Annotated
from pydantic import BaseModel, ConfigDict, AfterValidator


def validate_latitude(lat: float):
    """
    Latitude field validator
    """
    if lat is None or not isinstance(lat, (float, int)) or lat < -90 or lat > 90:
        raise ValueError("latitude value must be between -90 and 90")
    return lat


def validate_longitude(lon: float):
    """
    Longitude field validator
    """
    if lon is None or not isinstance(lon, (float, int)) or lon < -180 or lon > 180:
        raise ValueError("longitude value must be between -180 and 180")
    return lon


Latitude = Annotated[float, AfterValidator(validate_latitude)]
Longitude = Annotated[float, AfterValidator(validate_longitude)]


class AddressBase(BaseModel):
    """
    Base model of Address entity
    """
    name: str
    street: str
    city: str
    state: str
    country: str
    latitude: Latitude
    longitude: Longitude


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
