import uuid

from datetime import datetime

from sqlalchemy import DateTime,Boolean
from sqlalchemy.orm import Mapped,mapped_column

from app.database.base import Base


class BaseModel(Base):

    __abstract__=True

    id:Mapped[str]=mapped_column(
        primary_key=True,
        default=lambda:str(uuid.uuid4())
    )

    created_at:Mapped[datetime]=mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at:Mapped[datetime]=mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    is_active:Mapped[bool]=mapped_column(
        Boolean,
        default=True
    )

    is_deleted:Mapped[bool]=mapped_column(
        Boolean,
        default=False
    )