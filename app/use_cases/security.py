from datetime import timedelta, datetime
import jwt


SECRET_KEY = "123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MIN = 30


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Создание JWT токена, кодирование данных
    :arg data: данные, которые будут вшиты в токен
    :arg expires_delta: задать уникальное время жизни токена, в ином случае будет использоваться ACCESS_TOKEN_EXPIRE_MIN
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str) -> dict:
    """Проверка входящего JWT-токена, декодирование"""
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload
