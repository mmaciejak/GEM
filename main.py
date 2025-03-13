from fastapi import FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select

import uuid
from models import (
    Person,
    PersonUpdate,
    PersonPublic,
    Accommodation,
    UpdateAccommodation,
    AccommodationPublic,
    AccommodationCreate,
    PersonCreate,
)

from fastapi.encoders import jsonable_encoder

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()

persons = []
accommodations = []

tags_metadata = [
    {"name": "Persons", "description": "Guests ans staff"},
    {"name": "Accommodations", "description": "Accommodations for Persons"},
    {"name": "Categories", "description": "Categories of guests and staff"},
    {"name": "Rules", "description": "Rules for Handouts"},
    {"name": "Users", "description": "Users of the system"},
]


def update_field(new_value, current_value):
    return new_value if new_value is not None else current_value

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Persons 
@app.get("/persons", tags=["Persons"])
async def read_persons():
    with Session(engine) as session:
        persons = session.exec(select(Person)).all()
        return persons


@app.get("/person/{id}", response_model=PersonPublic, tags=["Persons"])
async def read_person(id):
    try:
        person = persons[uuid.UUID(id)]
        return person
    except Exception as e:
        raise HTTPException(status_code=404, detail="Item not found") from e


@app.post("/person", response_model=PersonPublic, tags=["Persons"])
async def add_person(person: PersonCreate):
    with Session(engine) as session:
        session.add(person)
        session.commit()
        session.refresh(person)
    return person


@app.patch("/person/{id}", response_model=PersonPublic, tags=["Persons"])
async def update_person(id, update_person: PersonUpdate):
    stored_person_data = persons[uuid.UUID(id)]
    stored_person_model = Person(**stored_person_data)
    update_data = update_person.model_dump(exclude_unset=True)
    updated_person = stored_person_model.model_copy(update=update_data)
    persons[id] = jsonable_encoder(updated_person)
    return updated_person


@app.delete("/person/{id}", tags=["Persons"])
async def delete_person(id):
    del persons[uuid.UUID(id)]


# Accommodations


@app.get("/accommodations", tags=["Accommodations"])
async def read_accomodations(limit: int = 1000):
    return accommodations


@app.get("/accommodation/{id}", response_model=AccommodationPublic, tags=["Accommodations"])
async def read_accomodation(id):
    try:
        accommodation = accommodations[uuid.UUID(id)]
        return accommodation
    except Exception as e:
        raise HTTPException(status_code=404, detail="Item not found") from e


@app.post("/accommodation", response_model=AccommodationPublic, tags=["Accommodations"])
async def add_accommodation(accommodation: AccommodationCreate):
    # should be check for names overlap
    accommodations[uuid.uuid4] = jsonable_encoder(accommodation)
    return accommodation


@app.patch("/accommodation/{id}", response_model=AccommodationPublic, tags=["Accommodations"])
async def update_accommodation(id, update_accommodation: UpdateAccommodation):
    stored_accommodation_data = accommodations[uuid.UUID(id)]
    stored_accommodation_model = Accommodation(**stored_accommodation_data)
    update_data = update_accommodation.model_dump(exclude_unset=True)
    updated_accommodation = stored_accommodation_model.model_copy(update=update_data)
    accommodations[uuid.UUID(id)] = jsonable_encoder(updated_accommodation)
    return updated_accommodation


@app.delete("/accommodation/{id}", tags=["Accommodations"])
async def delete_accommodation(id):
    del accommodations[uuid.UUID(id)]


# Categories

# Rules

# Users
