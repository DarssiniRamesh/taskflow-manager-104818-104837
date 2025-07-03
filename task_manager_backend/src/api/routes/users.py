"""User registration and information endpoints.

Provides user registration endpoint and (future) user profile retrieval.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from .. import models, schemas, database

router = APIRouter(
    prefix='/users',
    tags=['users'],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# PUBLIC_INTERFACE
@router.post("/register", response_model=schemas.UserRead, summary="Register a new user", description="Creates a new user account.")
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """Register a new user with a unique username and email."""
    db_user = db.query(models.User).filter((models.User.username == user.username) | (models.User.email == user.email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    hashed_password = get_password_hash(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Optionally, add more user profile/fetch endpoints (not required for MVP)
