from fastapi import FastAPI, HTTPException
import uuid
from models import Person, UpdatePerson, Accommodation, UpdateAccommodation

from fastapi.encoders import jsonable_encoder

app = FastAPI()

tags_metadata = [
    {"name": "Persons", "description": "Guests ans staff"},
    {"name": "Accommodations", "description": "Accommodations for Persons"},
    {"name": "Categories", "description": "Categories of guests and staff"},
    {"name": "Rules", "description": "Rules for Handouts"},
    {"name": "Users", "description": "Users of the system"},
]

def update_field(new_value, current_value):
    return new_value if new_value is not None else current_value

persons = {
    uuid.uuid4(): jsonable_encoder(
        Person(
            first_name="John",
            last_name="Doe",
        )
    )
}

accommodations = {
    uuid.uuid4() : jsonable_encoder(
        Accommodation(
            name="Nitki",
            vouchered=True,
            adress="Nowa Sól"
        )
    )
}

#Persons

@app.get("/persons", tags=["Persons"])
async def read_persons(limit: int = 1000):
    return persons

@app.get("/person/{id}", response_model=Person, tags=["Persons"])
async def read_person(id):
    try: 
        person = persons[uuid.UUID(id)]
        return person
    except Exception as e:
        raise HTTPException(status_code=404, detail="Item not found") from e
    
@app.post("/person", response_model=Person, tags=["Persons"])
async def add_person(person: Person):
    persons[uuid.uuid4] = jsonable_encoder(person)
    return person

@app.patch("/person/{id}", response_model=Person, tags=["Persons"])
async def update_person(id, update_person : UpdatePerson):
    stored_person_data = persons[uuid.UUID(id)]
    stored_person_model = Person(**stored_person_data)
    update_data = update_person.model_dump(exclude_unset=True)
    updated_person = stored_person_model.model_copy(update=update_data)
    persons[id] = jsonable_encoder(updated_person)
    return updated_person


#Accommodations

@app.get("/accommodations", tags=["Accommodations"])
async def read_accomodations(limit: int = 1000):
    return accommodations

@app.get("/accommodation/{id}", response_model=Accommodation, tags=["Accommodations"])
async def read_accomodation(id):
    try: 
        accommodation = accommodations[uuid.UUID(id)]
        return accommodation
    except Exception as e:
        raise HTTPException(status_code=404, detail="Item not found") from e
    
@app.post("/accommodation", response_model=Accommodation, tags=["Accommodations"])
async def add_accommodation(accommodation: Accommodation):
    #should be check for names overlap
    accommodations[uuid.uuid4] = jsonable_encoder(accommodation)
    return accommodation

@app.patch("/accommodation/{id}", response_model=Accommodation, tags=["Accommodations"])
async def update_accommodation(id, update_accommodation:UpdateAccommodation):
    stored_accommodation_data = accommodations[uuid.UUID(id)]
    stored_accommodation_model = Accommodation(**stored_accommodation_data)
    update_data = update_accommodation.model_dump(exclude_unset=True)
    updated_accommodation = stored_accommodation_model.model_copy(update=update_data)
    accommodations[uuid.UUID(id)] = jsonable_encoder(updated_accommodation)
    return updated_accommodation

#Rules



#Users