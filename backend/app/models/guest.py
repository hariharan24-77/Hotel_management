from datetime import date
from sqlalchemy import Date, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class Guest(BaseModel):
    __tablename__ = "guests"

    name: Mapped[str] = mapped_column(
        String(100), 
        nullable=False, 
        index=True
        )
    
    phone: Mapped[str] = mapped_column(
        String(20), 
        nullable=False
        )
    
    email: Mapped[str] = mapped_column(
        String(150), 
        nullable=False
        )
    
    gender: Mapped[str] = mapped_column(
        String(30), 
        nullable=False
        )
    
    dob: Mapped[date] = mapped_column(
        Date, 
        nullable=False
        )
    
    address: Mapped[str] = mapped_column(
        Text, 
        nullable=False
        )
    
    id_proof_type: Mapped[str] = mapped_column(
        String(50), 
        nullable=False
        )
    
    id_proof_number: Mapped[str] = mapped_column(
        String(100), 
        unique=True, 
        nullable=False, 
        index=True
    )
