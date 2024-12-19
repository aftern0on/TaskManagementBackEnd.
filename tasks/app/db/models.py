from datetime import datetime, date
from sqlmodel import SQLModel, Field, Relationship


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: int = Field(default=None, primary_key=True, index=True)
    name: str
    description: str
    status: str
    priority: str
    deadline: datetime
    create_time: datetime = Field(default_factory=datetime.utcnow)
    last_update_time: datetime = Field(default_factory=datetime.utcnow)
    creator_id: int
    executor_id: int
    project: 'Project' = Relationship(back_populates='project')


class Project(SQLModel, table=True):
    __tablename__ = "projects"

    id: int = Field(default=None, primary_key=True, index=True)
    name: str
    description: str
    start_date: date = Field(default=None)
    end_date: date = Field(default=None)
    status: str
    priority: str
    creator_id: int
    users_ids = list[int]
    tasks: list[Task] | None = Relationship(back_populates='project')
