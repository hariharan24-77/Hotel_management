from datetime import datetime
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.core.dependencies import get_current_user
from app.database.connection import get_db
from app.models.billing import Invoice, Payment
from app.models.reservation import Reservation
from app.models.room import Room
from app.models.setting import HotelSetting
from app.schemas.billing import InvoiceCreate, PaymentCreate

router = APIRouter(prefix="/api", tags=["Billing and Payments"])


def ok(message, data=None):
    return {"success": True, "message": message, "data": data, "errors": None}


def invoice_query():
    return (
        select(Invoice)
        .options(
            selectinload(Invoice.reservation).selectinload(Reservation.guest),
            selectinload(Invoice.reservation).selectinload(Reservation.room),
            selectinload(Invoice.payments),
        )
        .where(Invoice.is_deleted.is_(False))
    )


def invoice_data(x):
    return {
        "id": str(x.id),
        "invoice_no": x.invoice_no,
        "reservation_id": str(x.reservation_id),
        "booking_id": x.reservation.booking_id,
        "guest_name": x.reservation.guest.name,
        "room_number": x.reservation.room.room_number,
        "room_charge": float(x.room_charge),
        "service_charge": float(x.service_charge),
        "tax": float(x.tax),
        "amount": float(x.amount),
        "paid_amount": float(x.paid_amount),
        "balance": float(x.amount - x.paid_amount),
        "payment_status": x.payment_status,
        "payments": [
            {
                "payment_no": p.payment_no,
                "amount": float(p.amount),
                "payment_method": p.payment_method,
                "date": p.created_at.isoformat(),
            }
            for p in x.payments
        ],
    }


@router.get("/billing/eligible-reservations")
async def eligible(db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    billed = select(Invoice.reservation_id).where(Invoice.is_deleted.is_(False))
    result = await db.execute(
        select(Reservation)
        .options(
            selectinload(Reservation.guest),
            selectinload(Reservation.room).selectinload(Room.room_type),
        )
        .where(
            Reservation.status == "Completed",
            Reservation.is_deleted.is_(False),
            Reservation.id.not_in(billed),
        )
    )
    return ok(
        "Eligible reservations retrieved",
        [
            {
                "id": str(x.id),
                "booking_id": x.booking_id,
                "guest_name": x.guest.name,
                "room_number": x.room.room_number,
                "check_in": x.check_in.isoformat(),
                "check_out": x.check_out.isoformat(),
                "nights": max((x.check_out - x.check_in).days, 1),
                "room_rate": float(x.room.room_type.base_price),
                "suggested_room_charge": float(
                    x.room.room_type.base_price
                    * max((x.check_out - x.check_in).days, 1)
                ),
            }
            for x in result.scalars().all()
        ],
    )


@router.get("/billing")
async def bills(db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    r = await db.execute(invoice_query().order_by(Invoice.created_at.desc()))
    return ok(
        "Invoices retrieved", [invoice_data(x) for x in r.scalars().unique().all()]
    )


@router.post("/billing", status_code=status.HTTP_201_CREATED)
async def create_bill(
    req: InvoiceCreate, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)
):
    reservation = await db.scalar(
        select(Reservation)
        .options(selectinload(Reservation.room).selectinload(Room.room_type))
        .where(
            Reservation.id == req.reservation_id,
            Reservation.status == "Completed",
            Reservation.is_deleted.is_(False),
        )
    )
    if not reservation:
        raise HTTPException(400, "Only completed reservations can be invoiced")
    if await db.scalar(
        select(Invoice).where(
            Invoice.reservation_id == req.reservation_id, Invoice.is_deleted.is_(False)
        )
    ):
        raise HTTPException(409, "An invoice already exists for this reservation")
    settings = await db.scalar(
        select(HotelSetting).where(HotelSetting.is_deleted.is_(False))
    )
    rate = (settings.gst + settings.service_tax) if settings else Decimal("0")
    room_charge = reservation.room.room_type.base_price * max(
        (reservation.check_out - reservation.check_in).days, 1
    )
    tax_amount = ((room_charge + req.service_charge) * rate / Decimal("100")).quantize(
        Decimal("0.01")
    )
    total = room_charge + req.service_charge + tax_amount
    x = Invoice(
        invoice_no=f"INV-{datetime.utcnow():%Y%m%d%H%M%S%f}",
        reservation_id=req.reservation_id,
        room_charge=room_charge,
        service_charge=req.service_charge,
        tax=tax_amount,
        amount=total,
        paid_amount=Decimal("0"),
        payment_status="Unpaid",
    )
    db.add(x)
    await db.commit()
    r = await db.execute(invoice_query().where(Invoice.id == x.id))
    return ok("Invoice created", invoice_data(r.scalar_one()))


@router.get("/billing/{bill_id}")
async def bill(
    bill_id: str, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)
):
    r = await db.execute(invoice_query().where(Invoice.id == bill_id))
    x = r.scalar_one_or_none()
    if not x:
        raise HTTPException(404, "Invoice not found")
    return ok("Invoice retrieved", invoice_data(x))


@router.get("/payments")
async def payments(db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    r = await db.execute(
        select(Payment)
        .options(
            selectinload(Payment.invoice)
            .selectinload(Invoice.reservation)
            .selectinload(Reservation.guest)
        )
        .where(Payment.is_deleted.is_(False))
        .order_by(Payment.created_at.desc())
    )
    return ok(
        "Payments retrieved",
        [
            {
                "id": str(x.id),
                "payment_no": x.payment_no,
                "invoice_no": x.invoice.invoice_no,
                "guest_name": x.invoice.reservation.guest.name,
                "amount": float(x.amount),
                "payment_method": x.payment_method,
                "date": x.created_at.isoformat(),
            }
            for x in r.scalars().all()
        ],
    )


@router.post("/payments", status_code=status.HTTP_201_CREATED)
async def pay(
    req: PaymentCreate, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)
):
    x = await db.scalar(
        select(Invoice).where(Invoice.id == req.bill_id, Invoice.is_deleted.is_(False))
    )
    if not x:
        raise HTTPException(404, "Invoice not found")
    settings = await db.scalar(
        select(HotelSetting).where(HotelSetting.is_deleted.is_(False))
    )
    enabled = (
        {"Cash": settings.cash, "UPI": settings.upi, "Card": settings.card}
        if settings
        else {"Cash": True, "UPI": True, "Card": True}
    )
    if not enabled[req.payment_method]:
        raise HTTPException(
            400, f"{req.payment_method} payments are disabled in Settings"
        )
    balance = x.amount - x.paid_amount
    if req.amount > balance:
        raise HTTPException(400, f"Payment exceeds remaining balance {balance}")
    p = Payment(
        payment_no=f"PAY-{datetime.utcnow():%Y%m%d%H%M%S%f}",
        bill_id=x.id,
        amount=req.amount,
        payment_method=req.payment_method,
    )
    db.add(p)
    x.paid_amount += req.amount
    x.payment_status = "Paid" if x.paid_amount == x.amount else "Partially Paid"
    await db.commit()
    return ok("Payment recorded", {"payment_no": p.payment_no})
