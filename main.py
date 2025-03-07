from fastapi import FastAPI, HTTPException
import uuid
from models import Person, NewPerson

app = FastAPI()

persons = [
    Person(
        id=uuid.uuid4(),
        first_name="John",
        last_name="Doe",
    )
]

@app.get("/persons",)
async def read_items(limit: int = 1000):
    return persons[:limit]

@app.get("/person/{person_id}", response_model=Person)
async def read_item(person_id):
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
        arrival=new_person.arrival,
        departure=new_person.departure,
        category=new_person.category,
        accomodation=new_person.accomodation
    )
    persons.append(person)
    return Person