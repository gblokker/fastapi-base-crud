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

**Note** the example is not optimized and purely exists to give insight into how the crud base works and to have a playground. The example includes a Docker container with PostgreSQL that automatically runs Alembic migrations on startup:

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

### 3. Install dependencies

```bash
python -m venv .venv
\.venv\Scripts\activate
poetry install
```

### 4. Run the Example

```bash
python example/example.py
```

This will demonstrate both synchronous and asynchronous CRUD operations using the `User` model.

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/my-feature`).
3. Make your changes.
4. Ensure all tests pass (`pytest` recommended) (not applicable yet).
5. Open a Pull Request with a clear description of your changes.

Please follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines and include type hints where appropriate.

## License

See LICENSE file for details.

## Author

Goof Blokker - goofb@live.nl

## TODO:

- Add unittests.
- Make of example a devcontainer.
- Add support for bulk operations.
- Test for other python versions besides 3.13.