from fastapi import APIRouter

from managers.user import UserManager

router = APIRouter(tags=['auth'])


@router.post('/register/')
async def register(user_data):
    token = UserManager.register(user_data)