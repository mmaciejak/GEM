from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from sqlmodel import Field, Session, SQLModel, create_engine, select
import datetime

import uuid
from models import (
    Person,
    PersonUpdate,
    PersonPublic,
    PersonPublicWithRelations,
    Accommodation,
    UpdateAccommodation,
    AccommodationPublic,
    AccommodationCreate,
    AccomodationPublicWithPersons,
    PersonCreate,
    Category,
    CategoryUpdate,
    CategoryPublic,
    CategoryCreate,
    CategoryPubliWithRelations,
    HandOutRule,
    HandOutRuleCreate,
    HandOutRulePublic,
    HandOutRuleUpdate,
    HandOutRulePublicWithCategory
)
from database import get_by_str_id, add_new, update_by_str_id, delete_by_str_id, uuid_converter
from confirmation.generator import generate_pdf_confirmation

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

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
async def read_persons(session: Session = Depends(get_session),) -> list[PersonPublic]:
    persons = session.exec(select(Person)).all()
    return persons


@app.get("/person/{id}", response_model=PersonPublicWithRelations, tags=["Persons"])
async def read_person(*, session: Session = Depends(get_session), id: str):
    return get_by_str_id(Person, id, session)


@app.post("/person", response_model=PersonPublicWithRelations, tags=["Persons"], status_code=status.HTTP_201_CREATED)
async def add_person(*, session: Session = Depends(get_session), person: PersonCreate):
    return add_new(Person, person, session)


@app.patch("/person/{id}", response_model=PersonPublicWithRelations, tags=["Persons"])
async def update_person(*, session: Session = Depends(get_session), id: str, update_person: PersonUpdate):
    return update_by_str_id(Person, id, update_person, session)


@app.delete("/person/{id}", tags=["Persons"])
async def delete_person(*, session: Session = Depends(get_session), id):
    return delete_by_str_id(Person, id, session)

@app.post("person/check_in/{id}", tags=["Persons"])
async def check_in_person(*, session: Session = Depends(get_session), id):
    uuid_obj = uuid_converter(id)

    person_data = session.get(Person, uuid_obj)
    if not person_data:
        raise HTTPException(status_code=404, detail="Person not found")

    current_time_str =  datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    
    try:
        pdf_encoded_string = generate_pdf_confirmation(person_data.handout)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not generate pdf confirmation")
    
    update_dict = {
        "checked_in": True,
        "check_in_time": current_time_str
    }
    
    person_data.sqlmodel_update(update_dict)
    
    session.add(person_data)
    session.commit()
    session.refresh(person_data)
    
    #TODO set checked in status
    
    return pdf_encoded_string

# Accommodations
@app.get("/accommodations", tags=["Accommodations"])
async def read_accomodations(*, session: Session = Depends(get_session), limit: int = 1000) -> list[AccommodationPublic]:
    accommodations = session.exec(select(Accommodation)).all()
    return accommodations


@app.get("/accommodation/{id}", response_model=AccomodationPublicWithPersons, tags=["Accommodations"])
async def read_accomodation(*, session: Session = Depends(get_session), id: str):
    return get_by_str_id(Accommodation, id, session)


@app.post("/accommodation", response_model=AccomodationPublicWithPersons, tags=["Accommodations"], status_code=status.HTTP_201_CREATED)
async def add_accommodation(*, session: Session = Depends(get_session), accommodation: AccommodationCreate):
    return add_new(Accommodation, accommodation, session)


@app.patch("/accommodation/{id}", response_model=AccomodationPublicWithPersons, tags=["Accommodations"])
async def update_accommodation(*, session: Session = Depends(get_session), id, update_accommodation: UpdateAccommodation):
    return update_by_str_id(Accommodation, id, update_accommodation, session)


@app.delete("/accommodation/{id}", tags=["Accommodations"])
async def delete_accommodation(*, session: Session = Depends(get_session), id):
    return delete_by_str_id(Accommodation, id, session)


# Categories
@app.get("/categories", tags=["Categories"])
async def read_categories(*, session: Session = Depends(get_session), limit: int = 1000) -> list[CategoryPublic]:
    categories = session.exec(select(Category)).all()
    return categories


@app.get("/category/{id}", response_model=CategoryPubliWithRelations, tags=["Categories"])
async def read_category(*, session: Session = Depends(get_session), id: str):
    return get_by_str_id(Category, id, session)


@app.post("/category", response_model=CategoryPubliWithRelations, tags=["Categories"], status_code=status.HTTP_201_CREATED)
async def add_category(*, session: Session = Depends(get_session), category: CategoryCreate):
    return add_new(Category, category, session)


@app.patch("/category/{id}", response_model=CategoryPubliWithRelations, tags=["Categories"])
async def update_category(*, session: Session = Depends(get_session), id, update_category: CategoryUpdate):
    return update_by_str_id(Category, id, update_category, session)


@app.delete("/category/{id}", tags=["Categories"])
async def delete_category(*, session: Session = Depends(get_session), id):
    return delete_by_str_id(Category, id, session)


# HandOut Rules

@app.get("/handout_rules", tags=["Rules"])
async def read_rules(*, session: Session = Depends(get_session), limit: int = 1000) -> list[HandOutRulePublic]:
    categories = session.exec(select(HandOutRule)).all()
    return categories


@app.get("/handout_rule/{id}", response_model=HandOutRulePublicWithCategory, tags=["Rules"])
async def read_rule(*, session: Session = Depends(get_session), id: str):
    return get_by_str_id(HandOutRule, id, session)


@app.post("/handout_rule", response_model=HandOutRulePublicWithCategory, tags=["Rules"], status_code=status.HTTP_201_CREATED)
async def add_rule(*, session: Session = Depends(get_session), rule: HandOutRuleCreate):
    return add_new(HandOutRule, rule, session)


@app.patch("/handout_rule/{id}", response_model=HandOutRulePublicWithCategory, tags=["Rules"])
async def update_rule(*, session: Session = Depends(get_session), id, update_rule: HandOutRuleUpdate):
    return update_by_str_id(HandOutRule, id, update_rule, session)


@app.delete("/handout_rule/{id}", tags=["Rules"])
async def delete_rule(*, session: Session = Depends(get_session), id):
    return delete_by_str_id(HandOutRule, id, session)

# Users
