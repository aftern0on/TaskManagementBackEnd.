from app.db.models import Task
from app.repositories.repository import BaseRepository


class TaskRepository(BaseRepository[Task]):
    pass
