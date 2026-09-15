from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.dependencies import get_current_user
from app.database.connection import get_db
from app.models.guest import Guest
from app.models.reservation import Reservation
from app.models.room import Room
from app.schemas.reservation import ReservationCreate, ReservationUpdate

router = APIRouter(prefix="/api/reservations", tags=["Reservations"])


def response(message, data=None):
    return {"success": True, "message": message, "data": data, "errors": None}


def reservation_data(item: Reservation) -> dict:
    return {
        "id": str(item.id),
        "booking_id": item.booking_id,
        "guest_id": str(item.guest_id),
        "guest_name": item.guest.name,
        "room_id": str(item.room_id),
        "room_number": item.room.room_number,
        "check_in": item.check_in.isoformat(),
        "check_out": item.check_out.isoformat(),
        "adults": item.adults,
        "children": item.children,
        "special_request": item.special_request or "",
        "status": item.status,
    }


def reservation_query():
    return (
        select(Reservation)
        .options(selectinload(Reservation.guest), selectinload(Reservation.room))
        .where(Reservation.is_deleted.is_(False))
    )


async def validate_refs(db, guest_id, room_id):
    guest = await db.scalar(
        select(Guest).where(Guest.id == guest_id, Guest.is_deleted.is_(False))
    )
    room = await db.scalar(
        select(Room).where(
            Room.id == room_id, Room.is_deleted.is_(False), Room.is_active.is_(True)
        )
    )
    if not guest:
        raise HTTPException(400, "Invalid guest")
    if not room:
        raise HTTPException(400, "Invalid or inactive room")


async def ensure_room_available(db, room_id, check_in, check_out, exclude_id=None):
    conditions = [
        Reservation.room_id == room_id,
        Reservation.is_deleted.is_(False),
        Reservation.status != "Cancelled",
        Reservation.check_in < check_out,
        Reservation.check_out > check_in,
    ]
    if exclude_id:
        conditions.append(Reservation.id != exclude_id)
    if await db.scalar(select(Reservation.id).where(*conditions).limit(1)):
        raise HTTPException(409, "Room is already reserved for the selected dates")


async def lock_room_schedule(db, room_id):
    """Serialize availability checks for one room to prevent concurrent double booking."""
    await db.execute(select(func.pg_advisory_xact_lock(func.hashtext(str(room_id)))))


@router.get("")
async def list_reservations(
    db: AsyncSession = Depends(get_db), _user=Depends(get_current_user)
):
    result = await db.execute(
        reservation_query().order_by(Reservation.created_at.desc())
    )
    return response(
        "Reservations retrieved successfully",
        [reservation_data(x) for x in result.scalars().all()],
    )


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_reservation(
    request: ReservationCreate,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    await validate_refs(db, request.guest_id, request.room_id)
    await lock_room_schedule(db, request.room_id)
    await ensure_room_available(
        db, request.room_id, request.check_in, request.check_out
    )
    booking_id = f"RES-{datetime.utcnow():%Y%m%d%H%M%S%f}"
    values = request.model_dump()
    values["special_request"] = (values["special_request"] or "").strip() or None
    item = Reservation(**values, booking_id=booking_id, status="Pending")
    db.add(item)
    await db.commit()
    result = await db.execute(reservation_query().where(Reservation.id == item.id))
    return response(
        "Reservation created successfully", reservation_data(result.scalar_one())
    )


@router.get("/{reservation_id}")
async def get_reservation(
    reservation_id: str,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    result = await db.execute(
        reservation_query().where(Reservation.id == reservation_id)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(404, "Reservation not found")
    return response("Reservation retrieved successfully", reservation_data(item))


@router.put("/{reservation_id}")
async def update_reservation(
    reservation_id: str,
    request: ReservationUpdate,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    item = await db.scalar(
        select(Reservation).where(
            Reservation.id == reservation_id, Reservation.is_deleted.is_(False)
        )
    )
    if not item:
        raise HTTPException(404, "Reservation not found")
    await validate_refs(db, item.guest_id, request.room_id)
    if request.status != "Cancelled":
        await lock_room_schedule(db, request.room_id)
        await ensure_room_available(
            db, request.room_id, request.check_in, request.check_out, item.id
        )
    for field, value in request.model_dump().items():
        if field == "special_request":
            value = (value or "").strip() or None
        setattr(item, field, value)
    await db.commit()
    result = await db.execute(reservation_query().where(Reservation.id == item.id))
    return response(
        "Reservation updated successfully", reservation_data(result.scalar_one())
    )


@router.put("/{reservation_id}/cancel")
async def cancel_reservation(
    reservation_id: str,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    item = await db.scalar(
        select(Reservation).where(
            Reservation.id == reservation_id, Reservation.is_deleted.is_(False)
        )
    )
    if not item:
        raise HTTPException(404, "Reservation not found")
    item.status = "Cancelled"
    await db.commit()
    return response("Reservation cancelled successfully")
