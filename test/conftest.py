import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import database
from models import task_model
from main import app

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture()
def test_db():
    database.Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    database.Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def client(test_db):
    app.dependency_overrides[database.get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
