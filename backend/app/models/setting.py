from decimal import Decimal
from sqlalchemy import Boolean, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import BaseModel


class HotelSetting(BaseModel):
    __tablename__ = "hotel_settings"

    name: Mapped[str] = mapped_column(
        String(150), 
        nullable=False, 
        default="Hotel PMS"
        )
    
    phone: Mapped[str] = mapped_column(
        String(20), 
        nullable=False, 
        default=""
        )
    
    email: Mapped[str] = mapped_column(
        String(150), 
        nullable=False, 
        default=""
        )
    
    address: Mapped[str] = mapped_column(
        Text, 
        nullable=False, 
        default=""
        )
    
    gst: Mapped[Decimal] = mapped_column(
        Numeric(5, 2), 
        nullable=False, 
        default=0
        )
    
    service_tax: Mapped[Decimal] = mapped_column(
        Numeric(5, 2), 
        nullable=False, 
        default=0
    )

    cash: Mapped[bool] = mapped_column(
        Boolean, 
        nullable=False, 
        default=True
        )
    
    upi: Mapped[bool] = mapped_column(
        Boolean, 
        nullable=False, 
        default=True
        )
    
    card: Mapped[bool] = mapped_column(
        Boolean, 
        nullable=False, 
        default=True
        )
