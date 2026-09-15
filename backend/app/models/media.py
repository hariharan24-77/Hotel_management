from sqlalchemy import String,ForeignKey

from sqlalchemy.orm import Mapped,mapped_column

from app.models.base import BaseModel



class Media(BaseModel):

    __tablename__="media"


    file_name:Mapped[str]=mapped_column(
        String(255),
        nullable=False
    )


    file_path:Mapped[str]=mapped_column(
        String(500),
        nullable=False
    )


    file_type:Mapped[str]=mapped_column(
        String(100),
        nullable=False
    )


    file_size:Mapped[int]=mapped_column(
        nullable=False
    )


    module_name:Mapped[str]=mapped_column(
        String(100),
        nullable=False
    )


    module_id:Mapped[str]=mapped_column(
        String(100),
        nullable=True
    )


    uploaded_by:Mapped[str]=mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )