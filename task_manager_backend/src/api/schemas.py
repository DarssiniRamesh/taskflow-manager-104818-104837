"""Pydantic Schemas for User and Task API data validation."""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# User schemas
# PUBLIC_INTERFACE
class UserBase(BaseModel):
    username: str = Field(..., description="Unique username for the user")
    email: EmailStr = Field(..., description="User email address")


# PUBLIC_INTERFACE
class UserCreate(UserBase):
    password: str = Field(..., description="Password for the user")


# PUBLIC_INTERFACE
class UserRead(UserBase):
    id: int = Field(..., description="User ID")

    class Config:
        orm_mode = True


# PUBLIC_INTERFACE
class UserLogin(BaseModel):
    username: str = Field(..., description="Username of the user")
    password: str = Field(..., description="User password")


# Task schemas
# PUBLIC_INTERFACE
class TaskBase(BaseModel):
    title: str = Field(..., description="Title of the task")
    description: Optional[str] = Field(None, description="Optional description of the task")


# PUBLIC_INTERFACE
class TaskCreate(TaskBase):
    pass


# PUBLIC_INTERFACE
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, description="New title for the task")
    description: Optional[str] = Field(None, description="New description of the task")
    is_completed: Optional[bool] = Field(None, description="Mark task as completed or not")


# PUBLIC_INTERFACE
class TaskRead(TaskBase):
    id: int = Field(..., description="Task ID")
    is_completed: bool = Field(..., description="Completion status of the task")
    created_at: str = Field(..., description="Task creation datetime")
    updated_at: str = Field(..., description="Task last update datetime")
    owner_id: int = Field(..., description="ID of the task owner")

    class Config:
        orm_mode = True
