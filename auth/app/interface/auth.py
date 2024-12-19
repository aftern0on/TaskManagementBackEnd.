from fastapi import APIRouter, Depends

from app.entities.token import RefreshTokenEntity
from app.entities.user import UserEntity
from app.framework.dependencies import get_user_repo, get_token_repo, get_token_factory, get_auth_user
from app.framework.factory import TokenFactory
from app.framework.repository import TokenRepository, UserRepository
from app.interface.schemas import RegisterUser, LoginUser, RefreshToken, OutputUserData
from app.use_cases.auth_service import register_case, login_case, refresh_case, logout_case

router = APIRouter()


@router.post("/register/")
async def register(user: RegisterUser, user_repo: UserRepository = Depends(get_user_repo)):
    """Регистрация нового пользователя. Нельзя зарегистрировать пользователя с существующим username.
    Проверяется password и confirm_password."""
    new_user = await register_case(user.username, user.password, user.confirm_password, user_repo)
    return {"id": new_user.id, "username": new_user.username}


@router.post("/login/")
async def login(
        user: LoginUser,
        user_repo: UserRepository = Depends(get_user_repo),
        token_repo: TokenRepository = Depends(get_token_repo),
        token_fact: TokenFactory = Depends(get_token_factory)
):
    """Возвращает access и refresh токены для авторизации в системе.
    Время жизни access-токена: 15 минут, refresh-токена: 15 дней."""
    tokens: dict = await login_case(user.username, user.password, user_repo, token_repo, token_fact)
    return tokens


@router.post("/logout/")
async def logout(
        refresh_data: RefreshToken,
        token_repo: TokenRepository = Depends(get_token_repo),
        token_fact: TokenFactory = Depends(get_token_factory),
        user: UserEntity = Depends(get_auth_user)
):
    """Добавить access и refresh токены в черный список до их истечения.
    Такие токены нельзя будет использовать для получения новых токенов или авторизации.
    Со стороны frontend после этого требуется сброс токенов из хранилищ.
    Если refresh-токена у клиента нет - access токен просто истечет и пользователю все равно придется авторизоваться."""
    refresh: RefreshTokenEntity = await token_fact.decode_token(refresh_data.refresh, 'refresh')
    await logout_case(refresh, user, token_repo)
    return {"status": True}


@router.post("/refresh/")
async def refresh_token(
        refresh: RefreshToken,
        token_repo: TokenRepository = Depends(get_token_repo),
        token_fact: TokenFactory = Depends(get_token_factory)
):
    """Обновление токенов. Не требует авторизации, только refresh.
    Ранее использованный токен будет недействительный."""
    tokens: dict = await refresh_case(refresh.refresh, token_repo, token_fact)
    return tokens


@router.get('/user', response_model=OutputUserData)
async def get_user_data(user: UserEntity = Depends(get_auth_user)):
    """Защищенный метод для проверки функционала, возвращает основные данные о пользователе"""
    return user.get_user_data()
