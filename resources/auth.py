from fastapi import APIRouter

from managers.user import UserManager

router = APIRouter(tags=['auth'])


@router.post('/register/', status_code=201)
async def register(user_data):
    token = UserManager.register(user_data)

    return {
        "token": token
    }


@router.post("/login/")
async def login(user_data):
    token = UserManager.login(user_data)
    return {
        "token": token
    }
