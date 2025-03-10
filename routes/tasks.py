from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from models import task_model
from schemas import paginated_tasks_schema, task_schema
from config import database
from datetime import datetime, timezone
from typing import Optional

router = APIRouter()

@router.post("/", response_model=task_schema.Task)
def create_task(task: task_schema.TaskCreate, db: Session = Depends(database.get_db)):
    if task.created_at is None:
        task.created_at = datetime.now(timezone.utc)
    db_task = task_model.Task(**task.model_dump(exclude_unset=True))
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/{task_id}", response_model=task_schema.Task)
def get_task(task_id: int, db: Session = Depends(database.get_db)):
    db_task = db.query(task_model.Task).filter(task_model.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail='Tarea no encontrada')
    return db_task

@router.put("/{task_id}", response_model=task_schema.Task)
def update_task(task_id: int, task_updated: task_schema.TaskCreate, db: Session = Depends(database.get_db)):
    db_task = db.query(task_model.Task).filter(task_model.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail='Tarea no encontrada')
    for var, value in task_updated.model_dump().items():
        setattr(db_task, var, value) if value else None
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/{task_id}", response_model=task_schema.Task)
def delete_task(task_id: int, db: Session = Depends(database.get_db)):
    db_task = db.query(task_model.Task).filter(task_model.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail='Tarea no encontrada')
    db.delete(db_task)
    db.commit()
    return db_task

@router.get("/", response_model=paginated_tasks_schema.PaginatedTasksSchema)
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

    query = db.query(task_model.Task)
    
    if search:
        query = query.filter(
            or_(
                task_model.Task.title.ilike(f"%{search}%"),
                task_model.Task.description.ilike(f"%{search}%")
            )
        )

    if status:
        query = query.filter(task_model.Task.status == status)
    if priority:
        query = query.filter(task_model.Task.priority == priority)
    
    total_elements = query.count()
    total_pages = (total_elements + size - 1) // size
    
    offset = (page - 1) * size
    query = query.limit(size).offset(offset)
    
    tasks = query.all()
    
    return paginated_tasks_schema.PaginatedTasksSchema(
        content=tasks,
        first_page=(page == 1),
        last_page=(page == total_pages),
        page=page,
        total_elements=total_elements,
        total_pages=total_pages
    )