from app.db.database import AsyncSession
from app.db.models import Project
from app.repositories.repository import BaseRepository


class ProjectRepository(BaseRepository[Project]):
    def __init__(self, session: AsyncSession):
        super().__init__(Project, session)
