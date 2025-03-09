from sqlalchemy import Column, Integer, String, DateTime
from ..config.database import Base

class Task(Base):
    __tablename__ = "Tasks"
    
    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, index = True)
    description = Column(String)
    status = Column(String, index = True) # "Pendiente", "En progreso", "Finalizada"
    priority = Column(String) # "Alta", "Media", "Baja"
    created_at = Column(DateTime, index = True)
    