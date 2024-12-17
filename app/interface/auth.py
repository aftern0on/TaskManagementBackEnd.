from fastapi import APIRouter, Depends

from app.entities.user import UserEntity
from app.framework.dependencies import get_user_repo, get_token_repo, get_token_factory, get_current_user
from app.framework.factory import TokenFactory
from app.framework.repository import TokenRepository, UserRepository
from app.interface.schemas import RegisterUser, LoginUser, RefreshToken
from app.use_cases.auth_service import register_case, login_case, refresh_case

router = APIRouter()


@router.post("/register/")
async def register(user: RegisterUser, user_repo: UserRepository = Depends(get_user_repo)):
    new_user = await register_case(user.username, user.password, user.confirm_password, user_repo)
    return {"id": new_user.id, "username": new_user.username}


@router.post("/login/")
async def login(
        user: LoginUser,
        user_repo: UserRepository = Depends(get_user_repo),
        token_repo: TokenRepository = Depends(get_token_repo),
        token_fact: TokenFactory = Depends(get_token_factory)
):
    tokens: dict = await login_case(user.username, user.password, user_repo, token_repo, token_fact)
    return tokens


@router.post("/refresh/")
async def refresh_token(
        refresh: RefreshToken,
        token_repo: TokenRepository = Depends(get_token_repo),
        token_fact: TokenFactory = Depends(get_token_factory)
):
    tokens: dict = await refresh_case(refresh.refresh, token_repo, token_fact)
    return tokens


@router.get('/user')
async def get_user_data(user: UserEntity = Depends(get_current_user)):
    """Защищенный метод для проверки функционала, возвращает основные данные о пользователе"""
    user_data = user.__dict__
    del user_data['hashed_password']
    return user_data
