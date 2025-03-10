from fastapi import FastAPI
from config import database
from routes import tasks

database.create_database()

app = FastAPI()

app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
