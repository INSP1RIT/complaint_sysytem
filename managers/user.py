from passlib.context import CryptContext
from asyncpg import UniqueViolationError
from db_api import database
from managers.auth import AuthManager
from models import user
from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserManager:
    @staticmethod
    async def register(user_data):
        user_data['password'] = pwd_context.hash(user_data['password'])
        try:
            id_ = await database.execute(user.insert().values(**user_data))
        except UniqueViolationError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        user_obj = await database.fetch_one(user.select().where(user.c.id == id_))

        return AuthManager.encode_token(user_obj)

    @staticmethod
    async def login(user_data):
        user_obj = await database.fetch_one(user.select().where(user.c.email == user_data['email']))

        if not user_obj:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Wrong email passed"
            )
        elif not pwd_context.verify(user_obj['password'], user_obj['password']):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Wrong password or email"
            )

        return AuthManager.encode_token(user_obj)
