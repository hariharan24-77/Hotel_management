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