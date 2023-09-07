from passlib.context import CryptContext


pwd = CryptContext(schemes=['bcrypt'], depricated='auto')

class UserManager:
    async def register(self, user_data):
        user_data['password'] = None