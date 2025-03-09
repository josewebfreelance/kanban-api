from fastapi import FastAPI
from config import database

database.create_database()

app = FastAPI()
