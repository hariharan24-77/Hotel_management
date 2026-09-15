from typing import Literal
from pydantic import BaseModel, Field


class RoomCreate(BaseModel):

    room_number: str = Field(
        min_length=1, 
        max_length=30
        )
    
    floor: int = Field(
        ge=0, 
        le=200
        )
    
    room_type_id: str


class RoomUpdate(RoomCreate):
    status: Literal["Available", "Occupied", "Maintenance", "Inactive"]
