from datetime import date
from pydantic import BaseModel, EmailStr, Field, field_validator


class GuestData(BaseModel):

    name: str = Field(
        min_length=2, 
        max_length=100
        )
    
    phone: str = Field(
        pattern=r"^[0-9]{10}$"
        )
    
    email: EmailStr

    gender: str = Field(
        min_length=2, 
        max_length=30
        )
    
    dob: date

    address: str = Field(
        min_length=5, 
        max_length=1000
        )
    
    id_proof_type: str = Field(
        min_length=2, 
        max_length=50
        )
    
    id_proof_number: str = Field(
        min_length=3, 
        max_length=100
        )

    @field_validator("dob")
    @classmethod
    def validate_dob(cls, value: date) -> date:
        if value >= date.today():
            raise ValueError("Date of birth must be before today")
        if value.year < date.today().year - 120:
            raise ValueError("Enter a valid date of birth")
        return value


class GuestCreate(GuestData):
    pass


class GuestUpdate(GuestData):
    pass
