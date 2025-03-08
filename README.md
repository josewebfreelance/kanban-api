# Proyecto API REST con FastAPI, SQLite y SQLAlchemy

Este proyecto es una API RESTful construida con FastAPI, utilizando SQLite como base de datos y SQLAlchemy como ORM.

## Configuración

1.  Crea un entorno virtual: `python3 -m venv kanban-api-env`
2.  Activa el entorno virtual: `source kanban-api-env/bin/activate` (Linux/macOS) o `kanban-api-env\Scripts\activate` (Windows)
3.  Instala las dependencias: `pip install -r requirements.txt`
4.  Crea un archivo `.env` en la raíz del proyecto y añade la siguiente línea: `DATABASE_URL=sqlite:///./kanban-api.db`
5.  Ejecuta la API: `uvicorn main:app --reload`

## Base de datos

* SQLite es una biblioteca integrada en Python, por lo que generalmente no se requiere instalación adicional.
* El archivo de la base de datos (`kanban-api.db`) se creará automáticamente en la carpeta del proyecto al ejecutar la API por primera vez.

## Tests

1. Para correr los test, primero instala pytest: `pip install pytest`
2. Luego corre los test desde la raíz del proyecto, con el comando: `pytest`

## Endpoints

* **Crear una tarea (POST /tasks/)**: Crea una nueva tarea.
* **Leer una tarea (GET /tasks/{task_id})**: Obtiene una tarea por su ID.
* **Actualizar una tarea (PUT /tasks/{task_id})**: Actualiza una tarea existente.
* **Eliminar una tarea (DELETE /tasks/{task_id})**: Elimina una tarea.
* **Listar tareas (GET /tasks/)**: Lista todos las tareas.

## Documentación

La documentación de la API se genera automáticamente y está disponible en `/docs` (Swagger UI) y `/redoc` (ReDoc).