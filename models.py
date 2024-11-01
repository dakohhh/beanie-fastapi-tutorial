import pendulum
from enum import Enum
from typing import Optional
from beanie import Document, before_event, Replace
from datetime import datetime
from pydantic import Field, BaseModel


class Priority(str, Enum):
    HIGH = "High"
    LOW = "Low"
    MEDIUM = "Medium"


class TaskInfo(Document):
    priority: Priority
    additional_value: int



class Task(Document):
    name: str = Field(max_length=100)
    description: str = Field(max_length=100)
    is_done: bool = False
    created_at: datetime = Field(default_factory=pendulum.now)
    updated_at: datetime = Field(default_factory=pendulum.now)


    @before_event(Replace)
    def update_timestamp(self):
       
        self.updated_at = datetime.now()

    class Settings:
        name = "tasks"



class TaskCreate(BaseModel):
    name: str = Field(max_length=100, example="Task 1")
    description: str = Field(max_length=100, example="A sample Content")


class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_done: Optional[bool] = None


