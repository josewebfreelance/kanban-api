from fastapi import status
from models import task_model
from schemas import task_schema
from datetime import datetime, timezone

def test_create_task(client):
    task_data = {"title": "Test Task", "description": "Test Description", "status": 1, "priority": 1}
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == status.HTTP_200_OK
    created_task = task_schema.Task(**response.json())
    assert created_task.title == "Test Task"
    assert created_task.description == "Test Description"
    assert created_task.status == 1
    assert created_task.priority == 1
    assert created_task.created_at is not None

def test_get_task(client, test_db):
    task_data = {"title": "Test Task", "description": "Test Description", "status": 1, "priority": 1}
    db_task = task_schema.TaskCreate(**task_data)
    db_task_model = task_model.Task(**db_task.model_dump(exclude_unset=True))
    test_db.add(db_task_model)
    test_db.commit()

    response = client.get(f"/tasks/{db_task_model.id}")
    assert response.status_code == status.HTTP_200_OK
    retrieved_task = task_schema.Task(**response.json())
    assert retrieved_task.id == db_task_model.id
    assert retrieved_task.title == "Test Task"

def test_update_task(client, test_db):
    task_data = {"title": "Test Task", "description": "Test Description", "status": 1, "priority": 1}
    db_task = task_schema.TaskCreate(**task_data)
    db_task_model = task_model.Task(**db_task.model_dump(exclude_unset=True))
    test_db.add(db_task_model)
    test_db.commit()

    updated_task_data = {"title": "Updated Task", "description": "Updated Description", "status": 2, "priority": 2}
    response = client.put(f"/tasks/{db_task_model.id}", json=updated_task_data)
    assert response.status_code == status.HTTP_200_OK
    updated_task = task_schema.Task(**response.json())
    assert updated_task.id == db_task_model.id
    assert updated_task.title == "Updated Task"
    assert updated_task.status == 2

def test_delete_task(client, test_db):
    task_data = {"title": "Test Task", "description": "Test Description", "status": 1, "priority": 1}
    db_task = task_schema.TaskCreate(**task_data)
    db_task_model = task_model.Task(**db_task.model_dump(exclude_unset=True))
    test_db.add(db_task_model)
    test_db.commit()

    response = client.delete(f"/tasks/{db_task_model.id}")
    assert response.status_code == status.HTTP_200_OK
    response = client.get(f"/tasks/{db_task_model.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_get_tasks_paginated(client, test_db):
    for i in range(25):
        task_data = {"title": f"Task {i}", "description": f"Description {i}", "status": 1, "priority": 1}
        db_task = task_schema.TaskCreate(**task_data)
        db_task_model = task_model.Task(**db_task.model_dump(exclude_unset=True))
        test_db.add(db_task_model)
    test_db.commit()

    response = client.get("/tasks/?size=10&page=1")
    assert response.status_code == status.HTTP_200_OK
    paginated_tasks = response.json()
    assert len(paginated_tasks["content"]) == 10
    assert paginated_tasks["page"] == 1
    assert paginated_tasks["total_elements"] == 25
    assert paginated_tasks["total_pages"] == 3

def test_get_tasks_filtered(client, test_db):
    task_data1 = {"title": "Test Task 1", "description": "Test Description 1", "status": 1, "priority": 1}
    task_data2 = {"title": "Test Task 2", "description": "Test Description 2", "status": 2, "priority": 2}
    db_task1 = task_model.Task(**task_schema.TaskCreate(**task_data1).model_dump(exclude_unset=True))
    db_task2 = task_model.Task(**task_schema.TaskCreate(**task_data2).model_dump(exclude_unset=True))
    test_db.add(db_task1)
    test_db.add(db_task2)
    test_db.commit()

    response = client.get("/tasks/?status=2")
    assert response.status_code == status.HTTP_200_OK
    filtered_tasks = response.json()["content"]
    assert len(filtered_tasks) == 1
    assert filtered_tasks[0]["status"] == 2

def test_get_tasks_search(client, test_db):
    task_data1 = {"title": "Find Me", "description": "Test Description 1", "status": 1, "priority": 1}
    task_data2 = {"title": "Test Task 2", "description": "Different Description", "status": 2, "priority": 2} 
    db_task1 = task_model.Task(**task_schema.TaskCreate(**task_data1).model_dump(exclude_unset=True))
    db_task2 = task_model.Task(**task_schema.TaskCreate(**task_data2).model_dump(exclude_unset=True))
    test_db.add(db_task1)
    test_db.add(db_task2)
    test_db.commit()

    response = client.get("/tasks/?search=Find")
    assert response.status_code == status.HTTP_200_OK
    filtered_tasks = response.json()["content"]
    assert len(filtered_tasks) == 1
    assert filtered_tasks[0]["title"] == "Find Me"