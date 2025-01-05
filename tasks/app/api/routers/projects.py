from fastapi import APIRouter, Depends

from app.db.models import Project
from app.dependencies import get_project_repo
from app.repositories.projects import ProjectRepository
from app.schemas.project import CreateProject, ResultGetProject, ResultCreateProject, PatchProject, ResultPatchProject

router = APIRouter(prefix='/project', tags=["project"])


@router.get("/{project_id}", response_model=ResultGetProject)
async def get_project(project_id: int, project_repo: ProjectRepository = Depends(get_project_repo)):
    """Получение проекта по его идентификатору"""
    project: Project = await project_repo.get_by_id(project_id, ["tasks"])
    return ResultGetProject.from_orm(project)


@router.patch("/{project_id}", response_model=ResultPatchProject)
async def patch_project(
        project_id: int, proj_patch: PatchProject, project_repo: ProjectRepository = Depends(get_project_repo)
):
    """Обновление существующего Project. Необязательно отправлять все поля, достаточно только обновленные"""
    project: Project = await project_repo.update(project_id, proj_patch.dict())
    return ResultPatchProject.from_orm(project)


@router.post("/", response_model=ResultCreateProject)
async def create_project(proj_create: CreateProject, project_repo: ProjectRepository = Depends(get_project_repo)):
    """Создание нового проекта, который будет содержать задачи"""
    new_project: Project = Project(**proj_create.dict(), creator_id=1)
    project: Project = await project_repo.create(new_project)
    return ResultCreateProject.from_orm(project)


@router.delete("/{project_id}")
async def delete_project(project_id: int, project_repo: ProjectRepository = Depends(get_project_repo)):
    """Удалить проект с указанным идентификатором"""
    project: Project = await project_repo.get_by_id(project_id, ["tasks"])
    await project_repo.delete(project)
    return project_id
