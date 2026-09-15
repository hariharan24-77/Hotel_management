<<<<<<< HEAD
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

class TokenUser(BaseModel):
    id: int
    full_name: str
    role: RoleEnum



class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: TokenUser

    
class RefreshRequest(BaseModel):
    refresh_token: str


class AccessTokenOnly(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: int | None = None
    role: str | None = None
=======
from pydantic import BaseModel,EmailStr



class LoginRequest(BaseModel):

    email:EmailStr

    password:str



class TokenResponse(BaseModel):

    access_token:str

    token_type:str

    role:str
    
    role_id : str
>>>>>>> sakthi
