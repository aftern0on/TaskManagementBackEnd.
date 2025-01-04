from fastapi import HTTPException, status


class BaseAPIError(HTTPException):
    """Базовый класс для всех пользовательских ошибок API."""
    def __init__(self, detail: str, status_code: int, code: str = "error", extra: str = None):
        """
        :param detail: Подробное описание ошибки.
        :param status_code: HTTP статус ошибки.
        :param code: Код ошибки для клиента (например, `auth_failed`).
        """
        body = {"message": detail, "code": code}
        if extra:
            body['extra'] = extra
        super().__init__(status_code=status_code, detail=body)


class ValidationError(BaseAPIError):
    def __init__(self, detail: str = "Invalid input", extra: str = None):
        super().__init__(
            detail=detail, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, code="validation_error", extra=extra)


class NotFoundError(BaseAPIError):
    def __init__(self, detail: str = "Resource not found", extra: str = None):
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND, code="not_found", extra=extra)


class ForbiddenError(BaseAPIError):
    def __init__(self, detail: str = "Action is forbidden", extra: str = None):
        super().__init__(detail=detail, status_code=status.HTTP_403_FORBIDDEN, code="forbidden", extra=extra)