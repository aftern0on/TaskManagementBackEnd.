from app.db.models import Project, Task
from app.exceptions import ForbiddenError


class ProjectMixins:
    class Permissions:
        """Миксин, отвечающий за проверку прав"""
        def p_is_creator(self, user_id: int, raise_error: bool = False) -> bool:
            """Проверить, что пользователь является владельцем проекта"""
            self: Project
            if self.creator_id != user_id:
                if raise_error:
                    raise ForbiddenError(f"The user with ID={user_id} is not the creator of the project ID={self.id}")
                return False
            return True

        def p_is_member(self, user_id: int, raise_error: bool = False) -> bool:
            """Проверить, что пользователь является членом"""
            self: Project
            if user_id not in self.users_ids:
                if raise_error:
                    raise ForbiddenError(
                        f"The user with ID={user_id} is neither the member of the project ID={self.id}"
                    )
                return False
            return True


class TaskMixins:
    class Permissions:
        """Миксин, отвечающий за проверку прав"""
        def p_is_creator(self, user_id: int, raise_error: bool = False) -> bool:
            """Проверить, что пользователь является создателем таска"""
            self: Task
            if self.creator_id != user_id:
                if raise_error:
                    raise ForbiddenError(f"The user with ID={user_id} is not the creator of the task ID={self.id}")
                return False
            return True
