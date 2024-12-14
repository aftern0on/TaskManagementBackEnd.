from fastapi import APIRouter, Depends, HTTPException
from jwt import InvalidTokenError

from app.dependencies import get_user_repo, get_refresh_token_repo
from app.interface.repository import IUserRepository, ITokenRepository
from app.interface.schemas import RegisterUser, LoginUser, RefreshToken
from app.use_cases.auth_service import RegisterUseCase, LoginUseCase, RefreshUseCase

router = APIRouter()


@router.post("/register/")
async def register(user: RegisterUser, user_repo: IUserRepository = Depends(get_user_repo)):
    case = RegisterUseCase(user_repo)
    try:
        new_user = await case.execute(user.username, user.password, user.confirm_password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"id": new_user.id, "username": new_user.username}


@router.post("/login/")
async def login(
        user: LoginUser, user_repo: IUserRepository = Depends(get_user_repo),
        token_repo: ITokenRepository = Depends(get_refresh_token_repo)):
    case = LoginUseCase(user_repo, token_repo)
    try:
        tokens: dict = await case.execute(user.username, user.password)
        return tokens
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/refresh/")
async def refresh_token(token: RefreshToken, token_repo: ITokenRepository = Depends(get_refresh_token_repo)):
    case = RefreshUseCase(token_repo)
    try:
        tokens = await case.execute(token.token)
        return tokens
    except InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=str(e))
