# fastapi-base-crud

An example of a base CRUD implementation for FastAPI that is built on Pydantic schemas and SQLAlchemy models. This library provides generic CRUD operations with both synchronous and asynchronous support.

## Features

- ✅ Generic CRUD base classes for SQLAlchemy models
- ✅ Type-safe operations using Python generics
- ✅ Pydantic schema validation
- ✅ Both sync and async support
- ✅ Filtering, pagination, and sorting capabilities
- ✅ PostgreSQL support with Alembic migrations

## Installation

```bash
poetry install
```

### Required Dependencies

- SQLAlchemy (ORM)
- Pydantic (Schema validation)
- Alembic (Database migrations)
- asyncpg (Async PostgreSQL driver)
- psycopg2-binary (Sync PostgreSQL driver)

## Running the Example

### 1. Start the PostgreSQL Database

The example includes a Docker container with PostgreSQL that automatically runs Alembic migrations on startup:

```bash
# Build the database image
docker build -f example/db.Dockerfile -t example-db example

# Run the container
docker run -d -p 5432:5432 --name test-postgres example-db

# Check logs to verify migrations ran
docker logs test-postgres
```

### 2. Configure Environment Variables

Copy the example environment file:

```bash
cp example/.env.example example/.env
```

The default values are:
```env
DB_USER=test_user
DB_PASSWORD=test_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=test_db
DB_ECHO=false
```

### 3. Run the Example

```bash
python example/example.py
```

This will demonstrate both synchronous and asynchronous CRUD operations using the `User` model.

## License

See LICENSE file for details.

## Author

Goof Blokker - goofb@live.nl
