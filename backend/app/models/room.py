from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class Room(BaseModel):
    __tablename__ = "rooms"

    room_number: Mapped[str] = mapped_column(
        String(30), 
        unique=True, 
        nullable=False, 
        index=True
        )

    
    floor: Mapped[int] = mapped_column(
        Integer, 
        nullable=False
        )
    
    room_type_id: Mapped[str] = mapped_column(
        ForeignKey("room_types.id"), 
        nullable=False
        )

    
    status: Mapped[str] = mapped_column(
        String(30), 
        nullable=False, 
        default="Available"
        )

    room_type = relationship("RoomType")
