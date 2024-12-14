import uuid
from datetime import timedelta, datetime
import jwt


SECRET_KEY = "123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MIN = 30
REFRESH_TOKEN_EXPIRE_DAYS = 15


def create_token(token_type: str, user_id: int = None, ttl: timedelta = None) -> [str, int]:
    """Создание JWT токена, кодирование данных
    :arg token_type: тип токена - access/refresh
    :arg data: данные, которые будут вшиты в токен
    :arg ttl: задать уникальное время жизни токена, в ином случае будет использоваться ACCESS_TOKEN_EXPIRE_MIN
    """

    if token_type == "access":
        expire = datetime.utcnow() + (ttl or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN))
        to_encode = dict(
            user=user_id,
            token_type=token_type,
            jti=str(uuid.uuid4()),
            iat=datetime.now().timestamp(),
            exp=expire.timestamp()
        )
    else:
        expire = datetime.utcnow() + (ttl or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
        to_encode = dict(jti=str(uuid.uuid4()))
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token, expire.timestamp()


def verify_token(token: str) -> dict | str:
    """Проверка входящего JWT-токена, декодирование"""
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload
