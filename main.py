from fastapi import FastAPI, HTTPException
import uuid
from models import Person, NewPerson, UpdatePerson, Accommodation, UpdateAccommodation

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

persons = [
    Person(
        id=uuid.uuid4(),
        first_name="John",
        last_name="Doe",
    )
]

accommodations = [
    Accommodation(
        id=uuid.uuid4(),
        name="Nitki",
        vouchered=True,
        adress="Nowa Sól"
    )
]

#Persons

@app.get("/persons", tags=["Persons"])
async def read_persons(limit: int = 1000):
    return persons[:limit]

@app.get("/person/{person_id}", response_model=Person, tags=["Persons"])
async def read_person(person_id):
    for person in persons:
        if str(person.id) == person_id:
            #calculate Handout
            return person
    raise HTTPException(status_code=404, detail="Item not found")
    
@app.post("/add_person", response_model=Person, tags=["Persons"])
async def add_person(new_person: NewPerson):
    person = Person(
        id=uuid.uuid4(),
        first_name=new_person.first_name,
        last_name=new_person.last_name,
        arrival=update_field(new_person.arrival, None),
        departure=update_field(new_person.departure, None),
        associated_movie=update_field(new_person.associated_movie, None),
        category=update_field(new_person.category, None),
        accommodation=update_field(new_person.accommodation, None)
    )
    persons.append(person)
    return person

@app.patch("/update_person/{update_person_id}", response_model=Person, tags=["Persons"])
async def update_person(update_person_id, update_person : UpdatePerson):
    for person in persons:
        if str(person.id) == update_person_id:
            person.first_name = update_field(update_person.first_name, person.first_name)
            person.last_name = update_field(update_person.last_name, person.last_name)
            person.arrival = update_field(update_person.arrival, person.arrival)
            person.departure = update_field(update_person.departure, person.departure)
            person.associated_movie = update_field(update_person.associated_movie, person.associated_movie)
            person.category = update_field(update_person.category, person.category)
            person.accommodation = update_field(update_person.accommodation, person.accommodation)
        return person
    
#Accommodations

@app.get("/accommodations", tags=["Accommodations"])
async def read_accomodations(limit: int = 1000):
    return accommodations[:limit]

@app.get("/accommodation/{id}", response_model=Accommodation, tags=["Accommodations"])
async def read_accomodation(id):
    for accommodation in accommodations:
        if  accommodation.id == id:
            return accommodation
    raise HTTPException(status_code=404, detail="Item not found")
    
@app.post("/add_accommodation", response_model=Accommodation, tags=["Accommodations"])
async def add_accommodation(new_accommodation: Accommodation):
    #should be check for names overlap
    accomodation = new_accommodation
    accommodations.append(accomodation)
    return accomodation

@app.patch("/update_accommodation/{id}", response_model=Accommodation, tags=["Accommodations"])
async def update_accommodation(id, update_accommodation:UpdateAccommodation):
    for accommodation in accommodations:
        if  accommodation.id == str(update_accommodation.id):
            accommodation.name = update_field(update_accommodation.name, accommodation.name)
            accommodation.address = update_field(update_accommodation.address, accommodation.address)
            accommodation.vouchered = update_field(update_accommodation.vouchered, accommodation.vouchered)

#Rules



#Users