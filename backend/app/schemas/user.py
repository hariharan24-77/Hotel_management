from pydantic import BaseModel,EmailStr



class MasterAdminCreate(BaseModel):

    name:str

    email:EmailStr

    password:str