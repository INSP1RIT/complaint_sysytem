from models import RoleType
from schemas import UserBase


class UserOut(UserBase):
    id: int
    first_name: str
    last_name: str
    phone: str
    role: RoleType
    iban: str
