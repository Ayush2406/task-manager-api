# Task Manager API

A backend REST API for managing user-specific tasks with JWT-based authentication and strict authorization.

This project focuses on correctness, clean architecture, and data integrity rather than frontend concerns.

---

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy Core (async)
- Alembic
- JWT (access tokens only)

---

## Features

- User registration and login with hashed passwords
- JWT-based authentication with token expiration
- Task ownership enforced at both database and query level
- Users can only create, read, update, and delete their own tasks
- Database-level constraints for data integrity
- Async I/O throughout the API
- Clean separation between routing, business logic, and persistence

---

## Project Structure

```text
app/
├── main.py                  # Application setup and router registration
├── database.py              # Async database engine and session dependency
├── tables.py                # SQLAlchemy Core table definitions
├── schemas.py               # Pydantic request/response schemas
├── routers/
│   ├── auth.py              # Authentication routes
│   └── tasks.py             # Task CRUD routes
├── core/
│   ├── jwt.py               # JWT creation and verification utilities
│   ├── security.py          # Password hashing utilities
│   └── errors.py            # Global exception handlers
├── dependencies/
│   ├── current_user.py      # Authentication / authorization dependency
│   └── pagination.py        # Pagination dependency
alembic/
├── versions/                # Alembic migration revisions
└── env.py                   # Alembic environment configuration
```

---

## Authentication

- Users authenticate using email and password.
- On successful login, the API issues a short-lived JWT access token.
- The access token must be sent with each protected request using the `Authorization` header.
- Tokens expire after 30 minutes and must be re-issued via login.

Example header:
Authorization: Bearer <access_token>

---

## Authorization Model

- Every task is owned by a single user.
- Ownership is enforced using a foreign key (`tasks.owner_id → users.id`).
- All task queries are scoped to the authenticated user.
- Users cannot access or modify tasks they do not own.
- Authorization is enforced in database queries, not in application logic after fetching data.

---

## Running Locally

### Prerequisites
- Python 3.11+
- PostgreSQL

### Setup

```bash
# create virtual environment
python -m venv env
source env/bin/activate

# install dependencies
pip install -r requirements.txt

# Environment Varibles
export SECRET_KEY=your_secret_key

# Database Migration
alembic upgrade head

# Start the Server
uvicorn app.main:app --reload

# The API will be available at:
http://localhost:8000
```
## Example Requests
### Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}'

### Get Tasks
curl http://localhost:8000/tasks \
  -H "Authorization: Bearer <access_token>"

## Notes
Refresh tokens are intentionally not implemented.

Task IDs are internal identifiers and are not intended to be user-facing.

The API prioritizes correctness and authorization over UI or UX concerns.
