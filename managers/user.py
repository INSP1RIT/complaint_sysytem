from passlib.context import CryptContext
from asyncpg import UniqueViolationError
from db_api import database
from managers.auth import AuthManager
from models import user
from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=['bcrypt'], depricated='auto')


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
