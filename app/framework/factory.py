import uuid
from datetime import datetime, timedelta

import jwt

from app.config import ACCESS_TOKEN_EXPIRE_MIN, REFRESH_TOKEN_EXPIRE_DAYS
from app.entities.token import RefreshTokenEntity, AccessTokenEntity, TokenEntity
from app.exceptions import ExpiredTokenError, InvalidTokenError


class TokenFactory:
    def __init__(self, secret_key: str, algorithm: str):
        self.secret_key = secret_key
        self.algorithm = algorithm

    async def create_token(self, token_type: str, user_id: int, exp: int = None, jti: str = None) -> TokenEntity:
        """Создание refresh/access токена"""
        token = None
        match token_type:
            case 'access':
                exp = exp or int((datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)).timestamp())
                token = AccessTokenEntity(None, exp, user_id, jti=jti)
            case 'refresh':
                exp = exp or int((datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)).timestamp())
                token = RefreshTokenEntity(None, exp, jti=jti)
        if not token:
            raise InvalidTokenError(extra=f"Current token type error: {token_type}")
        data = token.__dict__
        del data['value']
        token_value = jwt.encode(data, self.secret_key, algorithm=self.algorithm)
        token.value = token_value
        return token

    async def decode_token(self, token: str) -> AccessTokenEntity:
        """Декодирует JWT и возвращает данные"""
        try:
            data = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            if data.get('typ') != 'a':
                raise InvalidTokenError(extra='Unsuitable token type')
            return await self.access_token_from_dict(token, data)
        except jwt.exceptions.ExpiredSignatureError as e:
            raise ExpiredTokenError()
        except BaseException:
            raise InvalidTokenError()

    @staticmethod
    async def access_token_from_dict(token: str, data: dict[str, str | int]) -> AccessTokenEntity:
        """Создаёт AccessTokenEntity из словаря."""
        return AccessTokenEntity(
            value=token,
            exp=data["exp"],
            user_id=data["user_id"],
            jti=data["jti"]
        )
