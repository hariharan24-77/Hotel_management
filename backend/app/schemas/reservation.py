from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, model_validator


ReservationStatus = Literal["Pending", "Confirmed", "Checked-In", "Completed", "Cancelled"]


class ReservationDates(BaseModel):
    check_in: date
    check_out: date

    @model_validator(mode="after")
    def validate_dates(self):
        if self.check_out <= self.check_in:
            raise ValueError("Check-out date must be after check-in date")
        return self


class ReservationCreate(ReservationDates):

    guest_id: str = Field(
        min_length=1
        )
    
    room_id: str = Field(
        min_length=1
        )
    
    adults: int = Field(
        ge=1, 
        le=20
        )
    
    children: int = Field(
        ge=0, le=20
        )
    
    special_request: str | None = Field(default=None, max_length=2000)


class ReservationUpdate(ReservationDates):

    room_id: str = Field(
        min_length=1
        )
    
    adults: int = Field(
        ge=1, 
        le=20
        )
    
    children: int = Field(
        ge=0, 
        le=20
        )
    
    special_request: str | None = Field(
        default=None, 
        max_length=2000
        )
    
    status: ReservationStatus
