
# Template for quick FastAPI program with Pydantic and Sqlalchemy (SQLlite).

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from pydantic import BaseModel

# Create the FastAPI application.
# The title appears in the automatically FastAPI generated documentation.
app = FastAPI(
    title="Items API",
    description="A simple REST API for managing items.",
    version="1.0.0"
)


# --------------------------------------------------
# DATABASE CONFIGURATION
# --------------------------------------------------

# SQLite database file. It will be created automatically if it doesn't exist.
DATABASE_URL = "sqlite:///./test.db"

# The engine manages the connection between SQLAlchemy and the database.
# check_same_thread=False allows SQLite connections to work with FastAPI's
# synchronous endpoints, which may run in different threads.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# SessionLocal is a factory that creates individual database sessions.
# Each API request gets its own session through the get_db() dependency.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base is the parent class for all SQLAlchemy database models.
Base = declarative_base()


# --------------------------------------------------
# DATABASE MODEL
# --------------------------------------------------

# SQLAlchemy model: describes how an item is stored in the database.
# This class represents a table called "items".
class Item(Base):
    __tablename__ = "items"

    # Primary key: uniquely identifies each item.
    # SQLite automatically generates this value when an item is inserted.
    id = Column(Integer, primary_key=True, index=True)

    # Item name. nullable=False means this field cannot be empty in the database.
    # index=True creates an index to help speed up searches.
    name = Column(String, nullable=False, index=True)

    # Description of the item.
    description = Column(String, nullable=False)


# Create database tables based on the SQLAlchemy models.
# Existing tables are left unchanged; this does not perform schema migrations.
Base.metadata.create_all(bind=engine)


# --------------------------------------------------
# DATABASE DEPENDENCY
# --------------------------------------------------

# FastAPI calls this function whenever an endpoint requests a database session.
def get_db():
    db = SessionLocal()

    try:
        # yield provides the session to the endpoint.
        yield db
    finally:
        # Always close the session after the request is finished.
        db.close()


# --------------------------------------------------
# PYDANTIC SCHEMAS
# --------------------------------------------------

# Defines the data clients must provide when creating an item.
# Pydantic automatically validates incoming request data.
class ItemCreate(BaseModel):
    name: str
    description: str


# Defines the structure of item data returned by the API.
# Unlike ItemCreate, this schema also includes the database-generated ID.
class ItemResponse(BaseModel):
    id: int
    name: str
    description: str

    # Allows Pydantic to read data directly from SQLAlchemy objects.
    model_config = {"from_attributes": True}


# --------------------------------------------------
# CREATE ITEM (POST)
# --------------------------------------------------

# POST /items/
# Receives item data, saves it to the database, and returns the created item.
@app.post(
    "/items/",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED
)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):

    # Convert the Pydantic object into a dictionary.
    # ** unpacks the dictionary into the SQLAlchemy model's constructor.
    # Equivalent to Item(name=item.name, description=item.description).
    item_data = item.model_dump()
    db_item = Item(**item_data)

    try:
        # Stage the new item for insertion into the database.
        db.add(db_item)

        # Commit the transaction to permanently save the item.
        db.commit()

        # Refresh the object to retrieve database-generated values, such as its ID.
        db.refresh(db_item)

    except Exception:
        # Undo the transaction if something goes wrong.
        db.rollback()
        raise

    return db_item


# --------------------------------------------------
# GET ALL ITEMS (GET)
# --------------------------------------------------

# GET /items/
# Retrieves every item currently stored in the database.
@app.get("/items/", response_model=list[ItemResponse])
def read_items(db: Session = Depends(get_db)):

    # Query the Item table and return all matching records.
    return db.query(Item).all()


# --------------------------------------------------
# GET ITEM BY ID (GET)
# --------------------------------------------------

# GET /items/{item_id}
# Retrieves one item using its unique database ID.
@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):

    # Search for the first item whose ID matches the requested ID.
    db_item = db.query(Item).filter(Item.id == item_id).first()

    # Return HTTP 404 if no matching item exists.
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )

    return db_item


# --------------------------------------------------
# DELETE ITEM (DELETE)
# --------------------------------------------------

# DELETE /items/{item_id}
# Finds and deletes an item using its ID.
@app.delete(
    "/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_item(item_id: int, db: Session = Depends(get_db)):

    # Find the item that should be deleted.
    db_item = db.query(Item).filter(Item.id == item_id).first()

    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )

    try:
        # Mark the item for deletion and commit the transaction.
        db.delete(db_item)
        db.commit()

    except Exception:
        db.rollback()
        raise

    # HTTP 204 means the operation succeeded and returns no response body.


# --------------------------------------------------
# START THE APPLICATION
# --------------------------------------------------

# This block runs only when this Python file is executed directly.
# Uvicorn starts the server and makes the API accessible locally.
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )
