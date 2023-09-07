from pydantic import BaseModel

class UserBase(BaseModel):
    email: str


class UserRegisterIn(UserBase):
    password: str
    phone: str
    first_name: str
    last_name: str
    iban: str


class UserLogIn(UserBase):
    password: str

#"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjcsImV4cCI6MTY5NDEyNDk5Nn0.np2ag3VAHSReKEJ5Q-J_eGUO2j2B2kVpjptC3d_DrCw"