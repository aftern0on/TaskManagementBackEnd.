from app.db.database import AsyncSession
from app.db.models import Task
from app.repositories.repository import BaseRepository


class TaskRepository(BaseRepository[Task]):
    def __init__(self, session: AsyncSession):
        super().__init__(Task, session)
