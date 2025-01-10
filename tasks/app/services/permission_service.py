from app.db.models import Project, Task
from app.exceptions import ForbiddenError


class PermissionService:
    @staticmethod
    async def is_creator(entity: Project | Task, user_id: int, raise_error: bool = False) -> bool:
        """Проверить, что пользователь является создателем"""
        if entity.creator_id != user_id:
            if raise_error:
                raise ForbiddenError(f"The user with ID={user_id} is not the creator of the entity ID={entity.id}")
            return False
        return True

    @staticmethod
    async def is_member(entity: Project, user_id: int, raise_error: bool = False) -> bool:
        """Проверить, что пользователь является членом"""
        if user_id not in entity.users_ids:
            if raise_error:
                raise ForbiddenError(f"The user with ID={user_id} is neither the member of the entity ID={entity.id}")
            return False
        return True
