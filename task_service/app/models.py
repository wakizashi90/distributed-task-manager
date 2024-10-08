from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Task(BaseModel):
    title: str
    description: Optional[str]
    assigned_to: Optional[str]
    status: str = "pending"
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime]
