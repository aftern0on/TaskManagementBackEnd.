from fastapi import APIRouter, Depends

from app.db.models import Project
from app.dependencies import get_project_repo
from app.repositories.projects import ProjectRepository
from app.schemas.project import CreateProject, GetProject, ResultCreateProject

router = APIRouter(prefix='/project', tags=["project"])


@router.get("/{project_id}", response_model=GetProject)
async def get_project(project_id: int, project_repo: ProjectRepository = Depends(get_project_repo)):
    """Получение проекта по его идентификатору"""
    project: Project = await project_repo.get_by_id(project_id, ["tasks"])
    return GetProject.from_orm(project)


@router.post("/", response_model=ResultCreateProject)
async def create_project(proj_create: CreateProject, project_repo: ProjectRepository = Depends(get_project_repo)):
    """Создание нового проекта"""
    new_project: Project = Project(**proj_create.dict(), creator_id=1)
    project: Project = await project_repo.create(new_project)
    return ResultCreateProject.from_orm(project)
