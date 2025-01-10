from fastapi import APIRouter, Depends

from app.db.models import Project
from app.dependencies import get_project_repo, get_auth_user_from_credentials
from app.exceptions import ForbiddenError
from app.repositories.projects import ProjectRepository
from app.schemas.auth import UserBase
from app.schemas.project import CreateProject, ResultGetProject, ResultCreateProject, PatchProject, ResultPatchProject

router = APIRouter(prefix='/project', tags=["project"])


@router.get("/{project_id}", response_model=ResultGetProject)
async def get_project(
        project_id: int,
        project_repo: ProjectRepository = Depends(get_project_repo),
        user: UserBase = Depends(get_auth_user_from_credentials)
):
    """Получение проекта по его идентификатору"""
    project: Project = await project_repo.get_by_id(project_id, ["tasks"])
    if project.creator_id != user.id or user.id not in project.users_ids:
        raise ForbiddenError(f"The user with ID={user.id} is neither the creator nor the participant of the project")
    return ResultGetProject.from_orm(project)


@router.patch("/{project_id}", response_model=ResultPatchProject)
async def patch_project(
        project_id: int, proj_patch: PatchProject, project_repo: ProjectRepository = Depends(get_project_repo),
        user: UserBase = Depends(get_auth_user_from_credentials)
):
    """Обновление существующего Project. Необязательно отправлять все поля, достаточно только обновленные"""
    project: Project = await project_repo.get_by_id(project_id)
    if project.creator_id != user.id:
        raise ForbiddenError(f"The user with ID={user.id} is not the creator of the project")
    updated_project: Project = await project_repo.update(project_id, proj_patch.dict())
    return ResultPatchProject.from_orm(updated_project)


@router.post("/", response_model=ResultCreateProject)
async def create_project(
        proj_create: CreateProject, project_repo: ProjectRepository = Depends(get_project_repo),
        user: UserBase = Depends(get_auth_user_from_credentials)
):
    """Создание нового проекта, который будет содержать задачи"""
    new_project: Project = Project(**proj_create.dict(), creator_id=user.id)
    project: Project = await project_repo.create(new_project)
    return ResultCreateProject.from_orm(project)


@router.delete("/{project_id}")
async def delete_project(
        project_id: int, project_repo: ProjectRepository = Depends(get_project_repo),
        user: UserBase = Depends(get_auth_user_from_credentials)
):
    """Удалить проект с указанным идентификатором"""
    project: Project = await project_repo.get_by_id(project_id, ["tasks"])
    if project.creator_id != user.id:
        raise ForbiddenError(f"The user with ID={user.id} is not the creator of the project")
    await project_repo.delete(project)
    return project_id
