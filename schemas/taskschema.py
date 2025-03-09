from pydantic import BaseModel
from typing import Optional


class TaskBase(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    description: str
    status: Optional[str] = None
    priority: Optional[str] = None
    created_at: str
    
class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    
    class Config:
        orm_mode = True