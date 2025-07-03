"""Task CRUD endpoints, secured with JWT authentication.

Users can only access, create, modify, or delete their own tasks.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, database
from .auth import get_current_user

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)

# PUBLIC_INTERFACE
@router.post("/", response_model=schemas.TaskRead, summary="Create a new task")
def create_task(task: schemas.TaskCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    """Creates a new task for the authenticated user."""
    db_task = models.Task(**task.dict(), owner_id=current_user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# PUBLIC_INTERFACE
@router.get("/", response_model=List[schemas.TaskRead], summary="List all user tasks")
def read_tasks(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    """Lists all tasks for the authenticated user."""
    return db.query(models.Task).filter(models.Task.owner_id == current_user.id).all()

# PUBLIC_INTERFACE
@router.get("/{task_id}", response_model=schemas.TaskRead, summary="Get a specific task by ID")
def read_task(task_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    """Fetch a specific task belonging to the authenticated user."""
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# PUBLIC_INTERFACE
@router.put("/{task_id}", response_model=schemas.TaskRead, summary="Update a task")
def update_task(task_id: int, task_data: schemas.TaskUpdate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    """Updates the specified task for the authenticated user."""
    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    for field, value in task_data.dict(exclude_unset=True).items():
        setattr(db_task, field, value)
    db.commit()
    db.refresh(db_task)
    return db_task

# PUBLIC_INTERFACE
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a task")
def delete_task(task_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    """Deletes a task belonging to the authenticated user."""
    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return None
