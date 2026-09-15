from decimal import Decimal
from pydantic import BaseModel, EmailStr, Field, model_validator


class HotelProfile(BaseModel):

    name: str = Field(
        min_length=2, 
        max_length=150
        )
    
    phone: str = Field(
        pattern=r"^[0-9+() -]{7,20}$"
        )
    
    email: EmailStr

    address: str = Field(
        min_length=5, 
        max_length=1000
        )


class TaxSetting(BaseModel):
    gst: Decimal = Field(
        ge=0, 
        le=100, 
        decimal_places=2
        )
    
    service_tax: Decimal = Field(
        ge=0, 
        le=100, 
        decimal_places=2
        )


class PaymentSetting(BaseModel):
    cash: bool
    upi: bool
    card: bool

    @model_validator(mode="after")
    def one_method(self):
        if not (self.cash or self.upi or self.card):
            raise ValueError("Enable at least one payment method")
        return self


class RoomSetting(BaseModel):
    room_type: str = Field(
        min_length=2, 
        max_length=100
        )
    
    price: Decimal = Field(
        gt=0, 
        decimal_places=2
        )
    
    capacity: int = Field(
        ge=1, 
        le=50
        )
