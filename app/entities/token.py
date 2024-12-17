import datetime
import uuid


class TokenEntity:
    def __init__(self, value: str, exp: int, jti: str = None):
        self.value: str = value
        self.exp: int = exp
        self.jti: str = jti or str(uuid.uuid4())
        self.iat: int = int(datetime.datetime.now().timestamp())
        self.typ: str = 'r'

    @property
    def ttl(self) -> int:
        now = datetime.datetime.now().timestamp()
        return max(int(self.exp - now), 0)

    async def is_expired(self) -> bool:
        return self.ttl == 0


class RefreshTokenEntity(TokenEntity):
    pass


class AccessTokenEntity(RefreshTokenEntity):
    def __init__(self, value: str, exp: int, user_id: int, jti: str = None):
        super().__init__(value, exp, jti)
        self.user_id: int = user_id
        self.typ: str = 'a'
