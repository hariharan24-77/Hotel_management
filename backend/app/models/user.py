<<<<<<< HEAD
import enum
from sqlalchemy import Column, Integer, String, Boolean, Enum
from app.database import Base


class RoleEnum(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    receptionist = "receptionist"
    cashier = "cashier"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.receptionist)
    is_active = Column(Boolean, default=True)
=======
from sqlalchemy import String,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column,relationship

from app.models.base import BaseModel


class User(BaseModel):

    __tablename__="users"


    name:Mapped[str]=mapped_column(
        String(100),
        nullable=False
    )


    email:Mapped[str]=mapped_column(
        String(150),
        unique=True,
        nullable=False,
        index=True
    )


    password:Mapped[str]=mapped_column(
        String(255),
        nullable=False
    )

    created_by:Mapped[str|None]=mapped_column(
    nullable=True
    )


    updated_by:Mapped[str|None]=mapped_column(
        nullable=True
    )


    role_id:Mapped[str]=mapped_column(
        ForeignKey("roles.id"),
        nullable=False
    )


    role=relationship(
        "Role",
        back_populates = "users"
    )

    username:Mapped[str|None]=mapped_column(
        String(100),
        unique=True,
        nullable=True,
        index=True
    )
>>>>>>> sakthi
