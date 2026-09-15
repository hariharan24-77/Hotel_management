from pydantic import BaseModel, EmailStr, Field


class StaffCreate(BaseModel):

    name: str = Field(
        min_length=2, 
        max_length=100
        )
    
    email: EmailStr

    username: str = Field(
        min_length=3, 
        max_length=100
        )
    
    password: str = Field(
        min_length=8
        )
    
    role_id: str


class StaffUpdate(BaseModel):
    name: str = Field(
        min_length=2, 
        max_length=100
        )
    
    email: EmailStr

    username: str = Field(
        min_length=3, 
        max_length=100
        )
    
    role_id: str
    
    is_active: bool
