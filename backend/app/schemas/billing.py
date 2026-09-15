from decimal import Decimal
from typing import Literal
from pydantic import BaseModel, Field


class InvoiceCreate(BaseModel):
    reservation_id: str = Field(
        min_length=1
        )
    
    room_charge: Decimal = Field(
        gt=0, 
        max_digits=12, 
        decimal_places=2
        )
    
    service_charge: Decimal = Field(
        ge=0, 
        max_digits=12, 
        decimal_places=2
        )
    
    tax: Decimal = Field(
        ge=0, 
        max_digits=12, 
        decimal_places=2
        )


class PaymentCreate(BaseModel):
    bill_id: str = Field(
        min_length=1
        )
    
    amount: Decimal = Field(
        gt=0, 
        max_digits=12, 
        decimal_places=2
        )
    
    payment_method: Literal["Cash", "UPI", "Card"]
