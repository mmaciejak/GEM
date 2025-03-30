from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
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
    Category,
    CategoryUpdate,
    CategoryPublic,
    CategoryCreate,
    
)
from database import get_by_str_id, add_new, update_by_str_id, delete_by_str_id

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
    {"name": "Handout", "description": "Items to hand out to persons"},
]


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# Persons
@app.get("/persons", tags=["Persons"])
async def read_persons() -> list[PersonPublic]:
    with Session(engine) as session:
        persons = session.exec(select(Person)).all()
        return persons


@app.get("/person/{id}", response_model=PersonPublic, tags=["Persons"])
async def read_person(id: str):
    return get_by_str_id(Person, id, engine)


@app.post("/person", response_model=PersonPublic, tags=["Persons"])
async def add_person(person: PersonCreate):
    return add_new(Person, person, engine)


@app.patch("/person/{id}", response_model=PersonPublic, tags=["Persons"])
async def update_person(id: str, update_person: PersonUpdate):
    return update_by_str_id(Person, id, update_person, engine)


@app.delete("/person/{id}", tags=["Persons"])
async def delete_person(id):
    return delete_by_str_id(Person, id, engine)


# Accommodations
@app.get("/accommodations", tags=["Accommodations"])
async def read_accomodations(limit: int = 1000) -> list[AccommodationPublic]:
    with Session(engine) as session:
        accommodations = session.exec(select(Accommodation)).all()
    return accommodations


@app.get("/accommodation/{id}", response_model=AccommodationPublic, tags=["Accommodations"])
async def read_accomodation(id: str):
    return get_by_str_id(Accommodation, id, engine)


@app.post("/accommodation", response_model=AccommodationPublic, tags=["Accommodations"])
async def add_accommodation(accommodation: AccommodationCreate):
    return add_new(Accommodation, accommodation, engine)


@app.patch("/accommodation/{id}", response_model=AccommodationPublic, tags=["Accommodations"])
async def update_accommodation(id, update_accommodation: UpdateAccommodation):
    return update_by_str_id(Accommodation, id, update_accommodation, engine)


@app.delete("/accommodation/{id}", tags=["Accommodations"])
async def delete_accommodation(id):
    return delete_by_str_id(Accommodation, id, engine)


# Categories
@app.get("/categories", tags=["Categories"])
async def read_categories(limit: int = 1000) -> list[CategoryPublic]:
    with Session(engine) as session:
        categories = session.exec(select(Category)).all()
    return categories


@app.get("/category/{id}", response_model=CategoryPublic, tags=["Categories"])
async def read_category(id: str):
    return get_by_str_id(Category, id, engine)


@app.post("/category", response_model=CategoryPublic, tags=["Categories"])
async def add_category(category: CategoryCreate):
    return add_new(Category, category, engine)


@app.patch("/category/{id}", response_model=CategoryPublic, tags=["Categories"])
async def update_category(id, update_category: CategoryUpdate):
    return update_by_str_id(Category, id, update_category, engine)


@app.delete("/category/{id}", tags=["Categories"])
async def delete_category(id):
    return delete_by_str_id(Category, id, engine)


# HandOut Rules

# Users
