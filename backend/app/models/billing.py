from decimal import Decimal
from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel


class Invoice(BaseModel):
    __tablename__ = "invoices"
    invoice_no: Mapped[str] = mapped_column(
        String(40), 
        unique=True, 
        nullable=False, 
        index=True
    )

    reservation_id: Mapped[str] = mapped_column(
        ForeignKey("reservations.id"), 
        unique=True, 
        nullable=False, 
        index=True
    )

    room_charge: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    service_charge: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), 
        nullable=False, 
        default=0
    )

    tax: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    paid_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), 
        nullable=False, 
        default=0
    )

    payment_status: Mapped[str] = mapped_column(
        String(20), 
        nullable=False, 
        default="Unpaid"
    )

    reservation = relationship("Reservation")
    payments = relationship("Payment", back_populates="invoice")


class Payment(BaseModel):
    __tablename__ = "payments"
    payment_no: Mapped[str] = mapped_column(
        String(40), 
        unique=True, 
        nullable=False, 
        index=True
    )

    bill_id: Mapped[str] = mapped_column(
        ForeignKey("invoices.id"), 
        nullable=False, 
        index=True
    )
    
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    payment_method: Mapped[str] = mapped_column(String(20), nullable=False)
    invoice = relationship("Invoice", back_populates="payments")
