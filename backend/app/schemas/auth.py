from pydantic import BaseModel, EmailStr
from app.models.user import RoleEnum


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: RoleEnum = RoleEnum.receptionist


class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: RoleEnum
    is_active: bool

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: RoleEnum


class TokenData(BaseModel):
    user_id: int | None = None
    role: str | None = None