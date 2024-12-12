from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_user_repo
from app.framework.repository import UserRepository
from app.interface.schemas import RegisterUser, LoginUser
from app.use_cases.auth_service import RegisterUseCase, LoginUseCase

router = APIRouter()


@router.post("/register/")
async def register(user: RegisterUser, user_repo: UserRepository = Depends(get_user_repo)):
    case = RegisterUseCase(user_repo)
    try:
        new_user = await case.execute(user.username, user.password, user.confirm_password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"id": new_user.id, "username": new_user.username}


@router.post("/login/")
async def login(user: LoginUser, user_repo: UserRepository = Depends(get_user_repo)):
    case = LoginUseCase(user_repo)
    try:
        token = await case.execute(user.username, user.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"token": token}
