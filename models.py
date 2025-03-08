import datetime
import uuid
from enum import Enum

from pydantic import BaseModel

class Accommodation(BaseModel):
    name: str
    vouchered: bool | None
    adress: str | None
    
class UpdateAccommodation(BaseModel):
    name: str | None
    vouchered: bool | None
    adress: str | None

class HandOutRule(BaseModel):
    prefered_accomodation: Accommodation 
    vouchers_value_per_day : int | None
    t_shirt: bool | None
    badge: bool | None
    program: bool | None
    confirmation : bool | None

class PersonCategory(BaseModel):
    name: str
    rule: HandOutRule

class HandOut(BaseModel):
    t_shirt: bool | None = None
    badge: bool | None = None
    voucher_value: int | None = None
    accomodation_vouchers: int | None = None
    program: bool | None = None
    confirmation: bool | None = None
    
class UpdatePerson(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    associated_movie : str | None = None
    arrival: datetime.date | None = None
    departure: datetime.date | None = None
    category: PersonCategory | None = None
    accommodation: Accommodation | None = None

class Person(BaseModel):
    first_name: str
    last_name: str
    associated_movie : str | None = None
    arrival: datetime.date | None = None
    departure: datetime.date | None = None
    category: PersonCategory | None = None
    accommodation: Accommodation | None = None
    handout: HandOut | None = None