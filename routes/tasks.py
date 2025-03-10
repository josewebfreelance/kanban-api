from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from models import taskmodel
from schemas import taskschema, paginatedtasksschema
from config import database
from datetime import datetime, timezone
from typing import List, Optional

router = APIRouter()

@router.post("/", response_model=taskschema.Task)
def create_task(task: taskschema.TaskCreate, db: Session = Depends(database.get_db)):
    if task.created_at is None:
        task.created_at = datetime.now(timezone.utc)
    db_task = taskmodel.Task(**task.dict(exclude_unset=True))
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/{task_id}", response_model=taskschema.Task)
def get_task(task_id: int, db: Session = Depends(database.get_db)):
    db_task = db.query(taskmodel.Task).filter(taskmodel.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail='Tarea no encontrada')
    return db_task

@router.put("/{task_id}", response_model=taskschema.Task)
def update_task(task_id: int, task_updated: taskschema.TaskCreate, db: Session = Depends(database.get_db)):
    db_task = db.query(taskmodel.Task).filter(taskmodel.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail='Tarea no encontrada')
    for var, value in task_updated.dict().items():
        setattr(db_task, var, value) if value else None
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/{task_id}", response_model=taskschema.Task)
def delete_task(task_id: int, db: Session = Depends(database.get_db)):
    db_task = db.query(taskmodel.Task).filter(taskmodel.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail='Tarea no encontrada')
    db.delete(db_task)
    db.commit()
    return db_task

@router.get("/", response_model=paginatedtasksschema.PaginatedTasksSchema)
def tasks(
    search: Optional[str] = Query(None, description="Busqueda opcional"),
    status: Optional[int] = Query(None, description="Filtro por estado"),
    priority: Optional[int] = Query(None, description="Filtro por prioridad"),
    size: Optional[int] = Query(None, description="Limite de registros"),
    page: Optional[int] = Query(None, description="Obtener datos por página"),
    db: Session = Depends(database.get_db)
):

    if size is None:
        size = 10
    if page is None:
        page = 1

    query = db.query(taskmodel.Task)
    
    if search:
        query = query.filter(
            or_(
                taskmodel.Task.title.ilike(f"%{search}%"),
                taskmodel.Task.description.ilike(f"%{search}%")
            )
        )
    if status:
        query = query.filter(taskmodel.Task.status == status)
    if priority:
        query = query.filter(taskmodel.Task.priority == priority)
    
    total_elements = query.count()
    total_pages = (total_elements + size - 1)
    
    offset = (page - 1) * size
    query = query.limit(size).offset(offset)
    
    tasks = query.all()
    
    return paginatedtasksschema.PaginatedTasksSchema(
        content=tasks,
        first_page=(page == 1),
        last_page=(page == total_pages),
        page=page,
        total_elements=total_elements,
        total_pages=total_pages
    )