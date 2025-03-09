from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import taskmodel
from schemas import taskschema
from config import database

router = APIRouter()

@router.post("/", response_model=taskschema.Task)
def create_task(task: taskschema.TaskCreate, db: Session = Depends(database.get_db)):
    db_task = taskmodel.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task
