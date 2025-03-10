from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    title: Optional[str] = None
    description: str
    status: Optional[int] = 1
    priority: Optional[int] = 1
    created_at: Optional[datetime] = None
    
class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    
    class Config:
        from_attributes = True