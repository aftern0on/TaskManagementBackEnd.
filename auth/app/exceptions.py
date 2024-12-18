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


# Ошибки авторизации
class AuthorizationError(BaseAPIError):
    def __init__(self, detail: str = "Authorization failed", extra: str = None):
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED, code="auth_failed", extra=extra)


class InvalidTokenError(BaseAPIError):
    def __init__(self, detail: str = "Invalid token", extra: str = None):
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED, code="invalid_token", extra=extra)


class ExpiredTokenError(BaseAPIError):
    def __init__(self, detail: str = "Token has expired", extra: str = None):
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED, code="token_expired", extra=extra)


# Ошибки регистрации
class RegistrationError(BaseAPIError):
    def __init__(self, detail: str = "Registration failed", extra: str = None):
        super().__init__(
            detail=detail, status_code=status.HTTP_400_BAD_REQUEST, code="registration_failed", extra=extra)


class EmailAlreadyExistsError(BaseAPIError):
    def __init__(self, detail: str = "Email is already registered", extra: str = None):
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST, code="email_exists", extra=extra)


# Общие ошибки
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
