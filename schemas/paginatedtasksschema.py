from pydantic import BaseModel
from typing import List
from schemas import taskschema

class PaginatedTasksSchema(BaseModel):
    content: List[taskschema.Task]
    first_page: bool
    last_page: bool
    page: int
    total_pages: int
    total_elements: int