import uuid
from fastapi import HTTPException
from sqlmodel import Session, SQLModel

def uuid_converter(str_uuid:str) -> uuid.UUID: 
    try:
        uuid_obj = uuid.UUID(str_uuid)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    return uuid_obj

def get_by_str_id(model: type[SQLModel], id: str, session: Session) -> SQLModel:
    """
    Fetch an object by its string ID from the database.

    Args:
        model: The SQLModel database model class.
        id: The string representation of the UUID.
        engine: The database engine used to create a session.

    Returns:
        The retrieved database object.

    Raises:
        HTTPException: If the object is not found.
    """ 
    uuid_obj = uuid_converter(id)

    item = session.get(model, uuid_obj)
    if not item:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    return item


def add_new(model: type[SQLModel], obj_data: SQLModel, session: Session) -> SQLModel:
    """
    Validates input data to a database model, adds it to the session,
    commits the transaction, and refreshes the object.

    Args:
        obj_type: The SQLModel database model class.
        obj_data: The input data instance (e.g., a Pydantic model).
        engine: The database engine used to create a session.

    Returns:
        The updated object after the commit and refresh operations.
    """
    db_obj = model.model_validate(obj_data)  # Convert input to DB model

    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_by_str_id(model: type[SQLModel], id: str, update_data: SQLModel, session: Session) -> SQLModel:
    """
    Update an object in the database by its string ID.

    Args:
        model: The SQLModel database model class.
        id: The string representation of the UUID.
        update_data: The update data model (e.g., a Pydantic model).
        engine: The database engine used to create a session.

    Returns:
        The updated object after applying the changes.

    Raises:
        HTTPException: If the object is not found.
    """
    uuid_obj = uuid_converter(id)

    db_obj = session.get(model, uuid_obj)
    if not db_obj:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")

    # Apply only provided updates
    update_dict = update_data.model_dump(exclude_unset=True)
    db_obj.sqlmodel_update(update_dict)

    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def delete_by_str_id(model: type[SQLModel], id: str, session:Session) -> dict:
    """
    Delete an object from the database by its string ID.

    Args:
        model: The SQLModel database model class.
        id: The string representation of the UUID.
        engine: The database engine used to create a session.

    Returns:
        A success message indicating deletion.

    Raises:
        HTTPException: If the object is not found.
    """
    uuid_obj = uuid_converter(id)

    db_obj = session.get(model, uuid_obj)
    if not db_obj:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")

    session.delete(db_obj)
    session.commit()
    return {"ok": True}


def batch_add_users():
    pass
