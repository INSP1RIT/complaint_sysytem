from fastapi import APIRouter

from managers.user import UserManager
from schemas import UserLogIn, UserRegisterIn

router = APIRouter(tags=['auth'])


@router.post('/register/', status_code=201)
async def register(user_data: UserRegisterIn):
    token = await UserManager.register(user_data.model_dump())

    return {
        "token": token
    }


@router.post("/login/")
async def login(user_data: UserLogIn):
    token = await UserManager.login(user_data.model_dump())
    return {
        "token": token
    }
