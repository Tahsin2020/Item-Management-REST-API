# Item Management REST API

A simple template backend application built with **FastAPI, SQLAlchemy, SQLite, and Pydantic**. This template demonstrates how to build a REST API that allows clients to create, retrieve, and delete items stored in a database.

## Features

- **Create Items:** Add new items to the database.
- **Retrieve All Items:** Get a list of all stored items.
- **Retrieve Item by ID:** Search for a specific item using its ID.
- **Delete Items:** Remove an item from the database.
- **Data Validation:** Validate incoming requests using Pydantic.
- **Database Integration:** Store and manage data using SQLAlchemy ORM and SQLite.
- **Interactive API Documentation:** Explore and test endpoints through Swagger UI.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| FastAPI | REST API framework |
| SQLAlchemy | Database ORM |
| SQLite | Relational database |
| Pydantic | Request validation and response schemas |
| Uvicorn | ASGI server |

## Project Structure

```text
item-management-api/
│
├── main.py          # FastAPI application and API endpoints
├── test.db          # SQLite database (generated automatically)
└── README.md        # Project documentation
```

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd item-management-api
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows:**
```bash
venv\Scripts\activate
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install fastapi uvicorn sqlalchemy pydantic
```

## Running the Application

Start the FastAPI server:

```bash
python main.py
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically generates interactive API documentation using Swagger UI.

Open the following URL in your browser:

```text
http://127.0.0.1:8000/docs
```

You can use this interface to test API endpoints without needing a separate API client.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/items/` | Create a new item |
| GET | `/items/` | Retrieve all items |
| GET | `/items/{item_id}` | Retrieve an item by ID |
| DELETE | `/items/{item_id}` | Delete an item by ID |

### Example Requests

#### Create an Item

**POST** `/items/`

Request body:

```json
{
    "name": "Laptop",
    "description": "A personal computer"
}
```

Example response:

```json
{
    "id": 1,
    "name": "Laptop",
    "description": "A personal computer"
}
```

#### Retrieve All Items

**GET** `/items/`

Example response:

```json
[
    {
        "id": 1,
        "name": "Laptop",
        "description": "A personal computer"
    }
]
```

#### Retrieve an Item by ID

**GET** `/items/1`

Example response:

```json
{
    "id": 1,
    "name": "Laptop",
    "description": "A personal computer"
}
```

#### Delete an Item

**DELETE** `/items/1`

A successful deletion returns:

```text
204 No Content
```

If an item does not exist, the API returns:

```json
{
    "detail": "Item not found"
}
```

## Database

This project uses SQLite as its database.

SQLAlchemy ORM maps Python classes to database tables, allowing the application to interact with database records using Python objects instead of writing SQL queries directly.

The database file (`test.db`) is generated automatically when the application starts.

## Concepts Demonstrated

This project provides practical experience with:

- REST API development and HTTP methods.
- FastAPI routing and dependency injection.
- SQLAlchemy ORM and database sessions.
- SQLite database integration.
- Pydantic data validation and serialization.
- HTTP status codes and exception handling.
- Basic CRUD operations.

## Future Improvements

- [ ] Implement `PUT` and `PATCH` endpoints to update items.
- [ ] Add pagination and filtering.
- [ ] Add automated tests using Pytest.
- [ ] Introduce PostgreSQL as an alternative database.
- [ ] Implement database migrations using Alembic.
- [ ] Add authentication and authorization using JWT.
- [ ] Containerize the application using Docker.

## License

This project is available for educational and personal portfolio purposes.
