from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.dependencies import get_current_user
from app.database.connection import get_db
from app.models.reservation import Reservation
from app.models.room import Room

router = APIRouter(prefix="/api", tags=["Check-in and Checkout"])


class ReservationAction(BaseModel):
    reservation_id: str
    id_proof_verified: bool = False


def data(x):
    return {
        "id": str(x.id),
        "booking_id": x.booking_id,
        "guest_name": x.guest.name,
        "room_number": x.room.room_number,
        "check_in": x.check_in.isoformat(),
        "status": x.status,
    }


async def items(db, statuses):
    result = await db.execute(
        select(Reservation)
        .options(selectinload(Reservation.guest), selectinload(Reservation.room))
        .where(Reservation.status.in_(statuses), Reservation.is_deleted.is_(False))
        .order_by(Reservation.check_in)
    )
    return {
        "success": True,
        "message": "Retrieved successfully",
        "data": [data(x) for x in result.scalars().all()],
        "errors": None,
    }


@router.get("/checkins/pending")
async def pending_checkins(
    db: AsyncSession = Depends(get_db), _=Depends(get_current_user)
):
    return await items(db, ["Pending", "Confirmed"])


@router.post("/checkins")
async def checkin(
    request: ReservationAction,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    x = await db.scalar(
        select(Reservation)
        .options(selectinload(Reservation.room))
        .where(
            Reservation.id == request.reservation_id, Reservation.is_deleted.is_(False)
        )
    )
    if not x or x.status not in ("Pending", "Confirmed"):
        raise HTTPException(400, "Reservation cannot be checked in")
    if not request.id_proof_verified:
        raise HTTPException(400, "Guest ID proof must be verified")
    room = await db.scalar(select(Room).where(Room.id == x.room_id).with_for_update())
    if room.status == "Occupied":
        raise HTTPException(
            409,
            "This room is still occupied; checkout the current guest before another check-in",
        )
    if room.status in ("Maintenance", "Inactive"):
        raise HTTPException(
            409, "This room is unavailable; assign another room before check-in"
        )
    x.status = "Checked-In"
    room.status = "Occupied"
    await db.commit()
    return {
        "success": True,
        "message": "Guest checked in successfully",
        "data": None,
        "errors": None,
    }


@router.get("/checkouts/pending")
async def pending_checkouts(
    db: AsyncSession = Depends(get_db), _=Depends(get_current_user)
):
    return await items(db, ["Checked-In"])


@router.post("/checkouts")
async def checkout(
    request: ReservationAction,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    x = await db.scalar(
        select(Reservation)
        .options(selectinload(Reservation.room))
        .where(
            Reservation.id == request.reservation_id, Reservation.is_deleted.is_(False)
        )
    )
    if not x or x.status != "Checked-In":
        raise HTTPException(400, "Only checked-in reservations can be checked out")
    room = await db.scalar(select(Room).where(Room.id == x.room_id).with_for_update())
    x.status = "Completed"
    room.status = "Available"
    await db.commit()
    return {
        "success": True,
        "message": "Guest checked out successfully",
        "data": None,
        "errors": None,
    }
