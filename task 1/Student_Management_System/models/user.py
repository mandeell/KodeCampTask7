from pydantic import EmailStr, BaseModel


class User(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    is_active: bool