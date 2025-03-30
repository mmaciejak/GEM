import datetime
import uuid

from sqlmodel import Field, SQLModel
 
class AccommodationBasae(SQLModel):
    name: str
    vouchered: bool | None
    adress: str | None

class Accommodation(AccommodationBasae, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

class AccommodationCreate(AccommodationBasae):
    pass

class AccommodationPublic(AccommodationBasae):
    id: uuid.UUID
    
class UpdateAccommodation(SQLModel):
    name: str | None
    vouchered: bool | None
    adress: str | None


class HandOutRuleBase(SQLModel):
    prefered_accomodation: uuid.UUID | None = None
    vouchers_value_per_day : int | None
    t_shirt: bool | None
    badge: bool | None
    program: bool | None
    confirmation : bool | None

class HandoutRule(HandOutRuleBase, table = True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    
class HandoutRuleCreate(HandOutRuleBase):
    pass

class HandoutRulePublic(HandOutRuleBase):
    id: uuid.UUID
    
class HandOutRuleUpdate(SQLModel):
    prefered_accomodation: uuid.UUID | None = None
    vouchers_value_per_day : int | None
    t_shirt: bool | None
    badge: bool | None
    program: bool | None
    confirmation : bool | None

class CategoryBase(SQLModel):
    name: str
    rule: uuid.UUID | None = None   

class Category(CategoryBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

class CategoryPublic(CategoryBase):
    id: uuid.UUID
    
class CategoryCreate(CategoryBase):
    pass
    
class CategoryUpdate(SQLModel):
    name: str | None = None   
    rule: uuid.UUID | None = None   

class HandOutBase(SQLModel):
    t_shirt: bool | None = None
    badge: bool | None = None
    voucher_value: int | None = None
    accomodation_vouchers: int | None = None
    program: bool | None = None
    confirmation: bool | None = None
    manualy_changed: bool = False
    
class HandOut(HandOutBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

class HandOutPublic(HandOutBase):
    id: uuid.UUID

class HandOutPublicUpdate(SQLModel):
    t_shirt: bool | None = None
    badge: bool | None = None
    voucher_value: int | None = None
    accomodation_vouchers: int | None = None
    program: bool | None = None
    confirmation: bool | None = None

class PersonBase(SQLModel):
    first_name: str
    last_name: str
    associated_movie : str | None = None
    arrival: datetime.date | None = None
    departure: datetime.date | None = None
    category: uuid.UUID | None = None
    accommodation: uuid.UUID | None = None
    handout: uuid.UUID | None = None
    checked_in: bool | None = None
    check_in_time: datetime.datetime | None = None
    notes: str | None = None

class Person(PersonBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

class PersonCreate(PersonBase):
    pass

class PersonPublic(PersonBase):
    id: uuid.UUID
    
class PersonUpdate(SQLModel):
    first_name: str | None = None
    last_name: str | None = None
    associated_movie : str | None = None
    arrival: datetime.date | None = None
    departure: datetime.date | None = None
    category: uuid.UUID | None = None
    accommodation: uuid.UUID | None = None
    handout: uuid.UUID | None = None
    checked_in: bool | None=None
    check_in_time: datetime.datetime | None = None
    notes: str | None = None