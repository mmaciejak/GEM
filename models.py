import datetime
import uuid
from enum import Enum

from pydantic import BaseModel

class PersonCategory(str, Enum):
    volunteer = "volunteer"
    organizer = "organizer"
    filmmaker = "filmmaker"
    guest = "guest"
    special_guest = "special_guest"
    vip = "vip"
    media = "media"

class Accomodation(BaseModel):
    name: str
    vouchered: bool
    adress: str | None

class HandOutRule(BaseModel):
    for_group: PersonCategory
    prefered_accomodation: Accomodation 
    vouchers_value_per_day : int | None
    t_shirt: bool | None
    badge: bool | None
    program: bool | None
    confirmation : bool | None
     
class HandOut(BaseModel):
    t_shirt: bool | None = None
    badge: bool | None = None
    voucher_value: int | None = None
    accomodation_vouchers: int | None = None
    program: bool | None = None
    confirmation: bool | None = None

class NewPerson(BaseModel):
    first_name: str
    last_name: str
    arrival: datetime.date | None = None
    departure: datetime.date | None = None
    category: PersonCategory | None = None
    accomodation: Accomodation | None = None
    
class UpdatePerson(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    arrival: datetime.date | None = None
    departure: datetime.date | None = None
    category: PersonCategory | None = None
    accomodation: Accomodation | None = None

class Person(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    arrival: datetime.date | None = None
    departure: datetime.date | None = None
    category: PersonCategory | None = None
    accomodation: Accomodation | None = None
    handout: HandOut | None = None