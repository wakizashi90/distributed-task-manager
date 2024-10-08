from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskCreate(BaseModel):
    title: str
    description: Optional[str]
    assigned_to: Optional[str]
    due_date: Optional[datetime]
