# Task Manager Backend (FastAPI)

This is the backend API for the Task Manager application. It is built with FastAPI and provides secure, JWT-based endpoints for user registration, authentication, and task management (create, read, update, delete).

---

## Table of Contents

- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [Running the Server](#running-the-server)
- [API Overview](#api-overview)
- [Architecture & Design](#architecture--design)
- [Development Notes](#development-notes)

---

## Features

- User registration and login with password hashing
- JWT authentication for protected endpoints
- CRUD operations for tasks (users can only access and modify their own tasks)
- SQLite database via SQLAlchemy (default)
- CORS support for frontend integration

---

## Setup Instructions

1. **Clone the repository and navigate to the backend directory:**

    ```bash
    cd task_manager_backend
    ```

2. **(Recommended) Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the server (development):**

    ```bash
    uvicorn src.api.main:app --reload --port 3001
    ```

    The API will be available at [http://localhost:3001](http://localhost:3001)

5. **API documentation available at:**

    - [Swagger UI](http://localhost:3001/docs)
    - [OpenAPI JSON](http://localhost:3001/openapi.json)

6. **Database:**  
    - Uses an SQLite file by default (`task_manager.db`).
    - No manual migration required for MVP—tables are created automatically on startup.

---

## API Overview

### Authentication

- `POST /auth/login`
    - Request: `{ "username": "<string>", "password": "<string>" }`
    - Response: `{ "access_token": "<JWT>", "token_type": "bearer" }`
- JWT token is required for all `/tasks` endpoints.

### Users

- `POST /users/register`
    - Registers a new user.
    - Request: `{ "username": "<string>", "email": "<email>", "password": "<string>" }`
    - Response: User object (id, username, email)
- (Future) Additional user profile endpoints can be easily added.

### Tasks (all endpoints require authentication)

- `GET /tasks`
    - List all tasks for the authenticated user.

- `POST /tasks`
    - Create a new task for the authenticated user.
    - Request: `{ "title": "<string>", "description": "<string (optional)>"}`
    - Response: Task object.

- `GET /tasks/{task_id}`
    - Get details for a specific task.

- `PUT /tasks/{task_id}`
    - Update an existing task.
    - Request: Any subset of `{ "title": ..., "description": ..., "is_completed": true/false }`

- `DELETE /tasks/{task_id}`
    - Delete task.

**All endpoints return standard HTTP status codes and error messages.**

---

## Architecture & Design

The backend consists of the following main modules:

- **Entry Point (`src/api/main.py`):**
    - Configures FastAPI application, CORS, OpenAPI info, and includes routers for `/users`, `/auth`, and `/tasks`.
    - Creates SQLite DB tables automatically at startup.

- **Database Layer (`src/api/database.py`, `models.py`):**
    - SQLAlchemy models for `User` and `Task` (with proper relationships).
    - Handles DB session lifecycle via dependency injection.

- **Routes / Endpoints (`routes/`):**
    - **`users.py`** – User registration endpoint.
    - **`auth.py`**  – Authentication, JWT generation, and current user dependency.
    - **`tasks.py`** – Task CRUD endpoints, all secured with JWT.

- **Schemas (`schemas.py`):**
    - Pydantic models for validation of users and tasks.

#### Component Relationship Diagram (Mermaid)

```mermaid
flowchart TD
    subgraph API Layer
      MAIN[[main.py]]
      USERS[[users.py]]
      AUTH[[auth.py]]
      TASKS[[tasks.py]]
    end
    subgraph DB
      DB[(SQLite DB)]
      MODELS[[models.py]]
      SCHEMAS[[schemas.py]]
      DATABASE[[database.py]]
    end

    MAIN --> USERS
    MAIN --> AUTH
    MAIN --> TASKS
    USERS --> MODELS
    AUTH --> MODELS
    TASKS --> MODELS
    MODELS --> DATABASE
    MAIN --> DATABASE
    TASKS --> SCHEMAS
    USERS --> SCHEMAS
    AUTH --> DATABASE
    DATABASE --> DB
```

#### Security

- Passwords are hashed using Bcrypt.
- JWT tokens are used for authentication. Tokens encode the username as the subject ("sub" claim).
- Endpoints related to tasks or user data require the JWT in the `Authorization: Bearer <token>` header.

#### Error Handling

- All endpoints return standard error objects with appropriate HTTP status codes (`401`, `404`, `400`).

---

## Development Notes

- For production use:
    - Move `SECRET_KEY` and database URL into environment variables.
    - Switch from SQLite to PostgreSQL or MySQL as needed.
    - Add Alembic migration scripts for schema evolution.
- To add features, see routers under `src/api/routes/`. Each is modular.
- See FastAPI docs: https://fastapi.tiangolo.com/

---
