import datetime
import uuid

from sqlmodel import Field, SQLModel, Relationship

# Accommodations

class AccommodationBase(SQLModel):
    name: str
    vouchered: bool | None
    adress: str | None

class Accommodation(AccommodationBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    persons: list["Person"] = Relationship(back_populates="accommodation")

class AccommodationCreate(AccommodationBase):
    pass

class AccommodationPublic(AccommodationBase):
    id: uuid.UUID
    
class UpdateAccommodation(SQLModel):
    name: str | None
    vouchered: bool | None
    adress: str | None

# Hand Out Rules

class HandOutRuleBase(SQLModel):
    vouchers_value_per_day : int | None
    t_shirt: bool | None
    badge: bool | None
    program: bool | None
    confirmation : bool | None

class HandOutRule(HandOutRuleBase, table = True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    category: list["Category"] = Relationship(back_populates="handout_rule")
    
class HandOutRuleCreate(HandOutRuleBase):
    pass

class HandOutRulePublic(HandOutRuleBase):
    id: uuid.UUID
    
    
class HandOutRuleUpdate(SQLModel):
    vouchers_value_per_day : int | None
    t_shirt: bool | None
    badge: bool | None
    program: bool | None
    confirmation : bool | None

# Categories

class CategoryBase(SQLModel):
    name: str
    handout_rule_id: uuid.UUID | None = Field(default=None, foreign_key="handoutrule.id")

class Category(CategoryBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    persons: list["Person"] = Relationship(back_populates="category")
    handout_rule: HandOutRule | None = Relationship(back_populates="category")

class CategoryPublic(CategoryBase):
    id: uuid.UUID
    
class CategoryCreate(CategoryBase):
    pass
    
class CategoryUpdate(SQLModel):
    name: str | None = None   
    handout_rule: uuid.UUID | None = None   

# Hand Outs

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
    persons: list["Person"] = Relationship(back_populates="handout")

class HandOutPublic(HandOutBase):
    id: uuid.UUID

class HandOutUpdate(SQLModel):
    t_shirt: bool | None = None
    badge: bool | None = None
    voucher_value: int | None = None
    accomodation_vouchers: int | None = None
    program: bool | None = None
    confirmation: bool | None = None

# Persons

class PersonBase(SQLModel):
    first_name: str
    last_name: str
    associated_movie : str | None = None
    arrival: datetime.date | None = None
    departure: datetime.date | None = None
    checked_in: bool | None = None
    check_in_time: datetime.datetime | None = None
    notes: str | None = None
    category_id: uuid.UUID | None = Field(default=None, foreign_key="category.id")
    accommodation_id: uuid.UUID | None = Field(default=None, foreign_key="accommodation.id")
    handout_id: uuid.UUID | None = Field(default=None, foreign_key="handout.id")

class Person(PersonBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    category: Category | None = Relationship(back_populates="persons")
    accommodation: Accommodation | None = Relationship(back_populates="persons")
    handout: HandOut | None = Relationship(back_populates="persons")

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
    category_id: uuid.UUID | None = None
    accommodation_id: uuid.UUID | None = None
    handout_id: uuid.UUID | None = None
    checked_in: bool | None=None
    check_in_time: datetime.datetime | None = None
    notes: str | None = None
    
# Public with relations

class CategoryPublicWitRule(CategoryPublic):
    handout_rule: HandOutRulePublic | None = None
    
class CategoryPubliWithRelations(CategoryPublicWitRule):
    persons: list[PersonPublic] = []

class AccomodationPublicWithPersons(AccommodationPublic):
    persons: list[PersonPublic] = []
    
class PersonPublicWithRelations(PersonPublic):
    category: CategoryPublicWitRule | None = None 
    accommodation: AccommodationPublic | None = None 
    handout: HandOutPublic | None = None 
    
class HandOutRulePublicWithCategory(HandOutRulePublic):
    categories: list["CategoryPublic"] | None = None