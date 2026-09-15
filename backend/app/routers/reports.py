from datetime import date, datetime, time
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_user
from app.database.connection import get_db
from app.models.billing import Payment
from app.models.room import Room

router = APIRouter(prefix="/api/reports", tags=["Reports"])


def ok(data):
    return {
        "success": True,
        "message": "Report retrieved successfully",
        "data": data,
        "errors": None,
    }


async def room_counts(db):
    total = (
        await db.scalar(select(func.count(Room.id)).where(Room.is_deleted.is_(False)))
        or 0
    )
    occupied = (
        await db.scalar(
            select(func.count(Room.id)).where(
                Room.is_deleted.is_(False), Room.status == "Occupied"
            )
        )
        or 0
    )
    available = (
        await db.scalar(
            select(func.count(Room.id)).where(
                Room.is_deleted.is_(False),
                Room.status == "Available",
                Room.is_active.is_(True),
            )
        )
        or 0
    )
    maintenance = (
        await db.scalar(
            select(func.count(Room.id)).where(
                Room.is_deleted.is_(False), Room.status.in_(["Maintenance", "Inactive"])
            )
        )
        or 0
    )
    return total, available, occupied, maintenance


async def revenue_series(db, start=None, end=None):
    stmt = select(
        func.to_char(Payment.created_at, "YYYY-MM").label("month"),
        func.coalesce(func.sum(Payment.amount), 0),
    ).where(Payment.is_deleted.is_(False))
    if start:
        stmt = stmt.where(Payment.created_at >= datetime.combine(start, time.min))
    if end:
        stmt = stmt.where(Payment.created_at <= datetime.combine(end, time.max))
    rows = (await db.execute(stmt.group_by("month").order_by("month"))).all()
    return [x[0] for x in rows], [float(x[1]) for x in rows]


@router.get("/dashboard")
async def dashboard(db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    total, available, occupied, _m = await room_counts(db)
    revenue = await db.scalar(
        select(func.coalesce(func.sum(Payment.amount), 0)).where(
            Payment.is_deleted.is_(False)
        )
    )
    return ok(
        {
            "total_rooms": total,
            "available_rooms": available,
            "occupied_rooms": occupied,
            "total_revenue": float(revenue or 0),
        }
    )


@router.get("/revenue")
async def revenue(
    from_date: date | None = Query(None, alias="from"),
    to_date: date | None = Query(None, alias="to"),
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    if from_date and to_date and to_date < from_date:
        raise HTTPException(400, "To date must be on or after from date")
    months, amounts = await revenue_series(db, from_date, to_date)
    return ok({"months": months, "amounts": amounts, "total": sum(amounts)})


@router.get("/occupancy")
async def occupancy(db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    total, available, occupied, maintenance = await room_counts(db)
    return ok(
        {
            "total": total,
            "occupied": occupied,
            "available": available,
            "maintenance": maintenance,
        }
    )
