from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routes import users, tasks, auth

tags_metadata = [
    {
        "name": "users",
        "description": "Operations related to user registration."
    },
    {
        "name": "auth",
        "description": "Authentication endpoints for login and token management."
    },
    {
        "name": "tasks",
        "description": "CRUD operations for managing tasks. All endpoints require authentication."
    },
]

app = FastAPI(
    title="Task Manager Backend API",
    description="A full REST API for task management with user authentication (JWT), registration, and CRUD task management.",
    version="1.0.0",
    openapi_tags=tags_metadata
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup if they do not exist
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# PUBLIC_INTERFACE
@app.get("/", tags=["users"])
def health_check():
    """Health check endpoint."""
    return {"message": "Healthy"}

# Include routers
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(tasks.router)
