from sqlalchemy import Column, Integer, String, DateTime, func
from config.database import Base

class Task(Base):
    __tablename__ = "Tasks"
    
    id = Column(Integer, primary_key = True, autoincrement = True, index = True)
    title = Column(String, nullable = False, index = True)
    description = Column(String, default = None, nullable = True)
    status = Column(Integer, default = 1, index = True) # 1 = "Pendiente", 2 = "En progreso", 3 = "Finalizada"
    priority = Column(Integer, default = 1) # 1 = "Alta", 2 = "Media", 3 = "Baja"
    created_at = Column(DateTime, server_default = func.now(), index = True)
    