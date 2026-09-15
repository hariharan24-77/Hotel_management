from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class Reservation(BaseModel):
    __tablename__ = "reservations"

    booking_id: Mapped[str] = mapped_column(
        String(30), unique=True, nullable=False, index=True
    )
    guest_id: Mapped[str] = mapped_column(
        ForeignKey("guests.id"), nullable=False, index=True
    )
    room_id: Mapped[str] = mapped_column(
        ForeignKey("rooms.id"), nullable=False, index=True
    )
    check_in: Mapped[date] = mapped_column(
        Date, 
        nullable=False
        )
    
    check_out: Mapped[date] = mapped_column(
        Date, 
        nullable=False
        )
    
    adults: Mapped[int] = mapped_column(
        Integer, 
        nullable=False, 
        default=1
        )
    
    children: Mapped[int] = mapped_column(
        Integer, 
        nullable=False, 
        default=0
        )
    
    special_request: Mapped[str | None] = mapped_column(
        Text, 
        nullable=True
        )
    
    status: Mapped[str] = mapped_column(
        String(30), 
        nullable=False, 
        default="Pending"
        )

    guest = relationship("Guest")
    room = relationship("Room")
