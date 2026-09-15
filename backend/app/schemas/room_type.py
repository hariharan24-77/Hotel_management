from decimal import Decimal
from pydantic import BaseModel, Field


class RoomTypeCreate(BaseModel):

    name: str = Field(
        min_length=2, 
        max_length=100
        )
    
    base_price: Decimal = Field(
        gt=0, 
        max_digits=12, 
        decimal_places=2
        )
    
    capacity: int = Field(
        gt=0, 
        le=20
        )
    
    bed_type: str = Field(
        min_length=2, 
        max_length=50
        )
    
    description: str | None = Field(
        default=None, 
        max_length=500
        )


class RoomTypeUpdate(RoomTypeCreate):
    is_active: bool
