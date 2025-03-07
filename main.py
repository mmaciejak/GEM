from fastapi import FastAPI, HTTPException
import uuid
from models import Person, NewPerson, UpdatePerson, Accomodation

app = FastAPI()

persons = [
    Person(
        id=uuid.uuid4(),
        first_name="John",
        last_name="Doe",
    )
]

accomodations = [
    Accomodation(
        name="Nitki",
        vouchered=True,
        adress="Nowa Sól"
    )
]

#Persons

@app.get("/persons",)
async def read_persons(limit: int = 1000):
    return persons[:limit]

@app.get("/person/{person_id}", response_model=Person)
async def read_person(person_id):
    for person in persons:
        if str(person.id) == person_id:
            #calculate Handout
            return person
    raise HTTPException(status_code=404, detail="Item not found")
    
@app.post("/add_person", response_model=Person)
async def add_person(new_person: NewPerson):
    person = Person(
        id=uuid.uuid4(),
        first_name=new_person.first_name,
        last_name=new_person.last_name,
        arrival=new_person.arrival if new_person.arrival is not None else None,
        departure=new_person.departure if new_person.departure is not None else None,
        category=new_person.category if new_person.category is not None else None,
        accomodation=new_person.accomodation if new_person.accomodation is not None else None
    )
    persons.append(person)
    return person

@app.patch("/update_person/{update_person_id}", response_model=Person)
async def update_person(update_person_id, update_person : UpdatePerson):
    for person in persons:
        if str(person.id) == update_person_id:
            person.first_name = update_person.first_name if update_person.first_name is not None else person.first_name
            person.last_name = update_person.last_name if update_person.last_name is not None else person.last_name
            person.arrival = update_person.arrival if update_person.arrival is not None else person.arrival
            person.departure = update_person.departure if update_person.arrival is not None else person.departure
            person.category = update_person.category if update_person.category is not None else person.category
            person.accomodation = update_person.accomodation if update_person.accomodation is not None else person.accomodation
        return person
    
#Accommodations

@app.get("/accommodations",)
async def read_accomodations(limit: int = 1000):
    return accomodations[:limit]

@app.get("/accommodation/{name}", response_model=Accomodation)
async def read_accomodation(name):
    for accomodation in accomodations:
        if  accomodation.name == name:
            return Accomodation
    raise HTTPException(status_code=404, detail="Item not found")
    
@app.post("/add_accommodation", response_model=Accomodation)
async def add_accommodation(new_accommodation: Accomodation):
    #should be check for names overlap
    accomodation = new_accommodation
    accomodations.append(accomodation)
    return accomodation

#Rules

#Users