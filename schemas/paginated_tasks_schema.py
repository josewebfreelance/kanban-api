from pydantic import BaseModel
from typing import List
from schemas import task_schema

class PaginatedTasksSchema(BaseModel):
    content: List[task_schema.Task]
    first_page: bool
    last_page: bool
    page: int
    total_pages: int
    total_elements: int