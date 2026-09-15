from decimal import Decimal
from sqlalchemy import Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class RoomType(BaseModel):
    __tablename__ = "room_types"

    name: Mapped[str] = mapped_column(
        String(100), 
        unique=True, 
        nullable=False, 
        index=True
        )
    
    base_price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), 
        nullable=False
        )
    
    capacity: Mapped[int] = mapped_column(
        Integer, 
        nullable=False
        )
    
    bed_type: Mapped[str] = mapped_column(
        String(50), 
        nullable=False
        )
    
    description: Mapped[str | None] = mapped_column(
        String(500), 
        nullable=True
        )
