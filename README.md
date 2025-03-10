# Proyecto API REST con FastAPI, SQLite y SQLAlchemy

Este proyecto es una API RESTful construida con FastAPI, utilizando SQLite como base de datos y SQLAlchemy como ORM.

### Características Principales

*   **Gestión Completa de Tareas:** Permite crear, leer, actualizar y eliminar tareas.
*   **Filtrado:** Ofrece la posibilidad de filtrar tareas por estado y prioridad.
*   **Búsqueda:** Permite buscar tareas por título o descripción.
*   **Paginación:** Implementa la paginación para gestionar eficientemente grandes cantidades de tareas.
*   **Autenticación:** Sistema de autenticación por token (JWT) para proteger los recursos.
*   **Gestión de usuarios:** Creación de usuarios con email y contraseña.
*   **Base de Datos:** Soporte para base de datos SQLite.
*   **Documentación Automática:** Generación automática de documentación con Swagger UI (`/docs`) y ReDoc (`/redoc`).

### Tecnologías Utilizadas

*   **FastAPI:** Framework web moderno y de alto rendimiento para la construcción de APIs con Python.
*   **SQLAlchemy:** ORM (Object-Relational Mapper) que facilita la interacción con la base de datos.
*   **SQLite:** Sistema de gestión de base de datos relacional integrado en Python.
*   **PyJWT:** Biblioteca para la creación y validación de JSON Web Tokens (JWT).
*   **Passlib:** Biblioteca para el manejo seguro de contraseñas.
*   **Bcrypt:** Algoritmo de hashing de contraseñas.
*   **Pydantic:** Biblioteca para la definición y validación de esquemas de datos.
*   **Uvicorn:** Servidor web ASGI para la ejecución de la API.
*   **pytest:** Framework para la realización de pruebas unitarias.
*   **Python-dotenv:** Para la gestión de las variables de entorno.

## Dependencias

### Dependencias de Producción

*   **`fastapi`:** Framework web para la construcción de APIs.
*   **`uvicorn`:** Servidor web ASGI para la ejecución de la API.
*   **`sqlalchemy`:** ORM para la interacción con la base de datos.
*   **`pydantic`:** Biblioteca para la definición y validación de esquemas de datos.
*   **`pyjwt`:** Biblioteca para la creación y validación de JSON Web Tokens (JWT).
*   **`passlib`:** Biblioteca para el manejo seguro de contraseñas.
*   **`bcrypt`:** Algoritmo de hashing de contraseñas.
*   **`python-dotenv`:** Para la gestión de las variables de entorno.

### Dependencias de Desarrollo

* **`pytest`:** Framework para la realización de pruebas unitarias.

### Explicación de Dependencias Relevantes

*   **FastAPI:** Facilita la creación de APIs de alto rendimiento con Python, ofreciendo características como la validación de datos, la documentación automática y la inyección de dependencias.
*   **SQLAlchemy:** Un ORM poderoso que permite interactuar con la base de datos mediante objetos de Python. Simplifica las operaciones CRUD (Create, Read, Update, Delete) y ofrece flexibilidad en el manejo de la base de datos.
*   **PyJWT:** Permite generar y validar tokens JWT, que son fundamentales para la autenticación y autorización de usuarios.
*   **Pydantic:** Esencial para la validación de datos de entrada y salida de la API, asegurando que los datos cumplan con los tipos y restricciones definidos.
*   **Passlib and bcrypt:** Proveen herramientas para el manejo seguro de contraseñas, mediante el hashing, lo que permite almacenar las contraseñas de manera segura en la base de datos.


## Instalación y Configuración

### Requisitos Previos

*   Python 3.8 o superior.
*   `pip` (gestor de paquetes de Python).
*   Un entorno virtual (recomendado).

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

## Endpoints de la API

### Tareas

*   **`POST /tasks/`**
    *   **Descripción:** Crea una nueva tarea.
    *   **Método:** `POST`
    *   **Parámetros de Entrada:**

        ```json
        {
          "title": "Mi Tarea",
          "description": "Descripción de la tarea",
          "status": 1,
          "priority": 2
        }
        ```
    *   **Respuesta (Ejemplo):**

        ```json
        {
            "id": 1,
            "title": "Mi Tarea",
            "description": "Descripción de la tarea",
            "status": 1,
            "priority": 2,
            "created_at": "2023-10-27T10:00:00"
        }
        ```

*   **`GET /tasks/`**
    *   **Descripción:** Obtiene una lista paginada de tareas.
    *   **Método:** `GET`
    *   **Parámetros de Consulta:**
        *   `search`: Término de búsqueda (opcional).
        *   `status`: Filtrar por estado (opcional).
        *   `priority`: Filtrar por prioridad (opcional).
        *   `size`: Número de tareas por página (opcional, por defecto: 10).
        *   `page`: Número de página (opcional, por defecto: 1).
    *   **Respuesta (Ejemplo):**

        ```json
        {
            "content": [
                {
                    "id": 1,
                    "title": "Tarea 1",
                    "description": "Descripción 1",
                    "status": 1,
                    "priority": 1,
                    "created_at": "2023-10-27T10:00:00"
                }
            ],
            "first_page": true,
            "last_page": true,
            "page": 1,
            "total_pages": 1,
            "total_elements": 1
        }
        ```

*   **`GET /tasks/{task_id}`**
    *   **Descripción:** Obtiene una tarea por su ID.
    *   **Método:** `GET`
    *   **Parámetros de Ruta:**
        *   `task_id`: ID de la tarea.
    *   **Respuesta (Ejemplo):**

        ```json
        {
            "id": 1,
            "title": "Tarea 1",
            "description": "Descripción 1",
            "status": 1,
            "priority": 1,
            "created_at": "2023-10-27T10:00:00"
        }

*   **`PUT /tasks/{task_id}`**
    *   **Descripción:** Actualiza una tarea.
    *   **Método:** `PUT`
    * **Parámetros de ruta**
        * `task_id`: ID de la tarea.
    *   **Parámetros de Entrada:**
        *   Misma estructura que `POST /tasks/`
    *   **Respuesta (Ejemplo):** Mismo estructura que `GET /tasks/{task_id}`

*   **`DELETE /tasks/{task_id}`**
    *   **Descripción:** Elimina una tarea.
    *   **Método:** `DELETE`
    * **Parámetros de ruta**
        * `task_id`: ID de la tarea.
    *   **Respuesta (Ejemplo):** Mismo estructura que `GET /tasks/{task_id}`


## Documentación

La documentación de la API se genera automáticamente y está disponible en `/docs` (Swagger UI) y `/redoc` (ReDoc).
