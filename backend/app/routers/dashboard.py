from fastapi import APIRouter, Depends
from sqlalchemy import inspect, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.database.connection import get_db

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


async def table_exists(db: AsyncSession, table_name: str) -> bool:
    connection = await db.connection()
    return await connection.run_sync(
        lambda sync_connection: inspect(sync_connection).has_table(table_name)
    )


async def count_rows(db: AsyncSession, table_name: str, where_sql: str = "") -> int:
    # Table/condition values are internal constants only, never request input.
    from sqlalchemy import text

    result = await db.execute(text(f"SELECT COUNT(*) FROM {table_name} {where_sql}"))
    return int(result.scalar_one())


@router.get("/summary")
async def dashboard_summary(
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    total_rooms = available_rooms = occupied_rooms = reservations = 0

    if await table_exists(db, "rooms"):
        total_rooms = await count_rows(db, "rooms", "WHERE is_deleted = false")
        available_rooms = await count_rows(
            db, "rooms", "WHERE is_deleted = false AND lower(status) = 'available'"
        )
        occupied_rooms = await count_rows(
            db, "rooms", "WHERE is_deleted = false AND lower(status) = 'occupied'"
        )

    if await table_exists(db, "reservations"):
        reservations = await count_rows(
            db,
            "reservations",
            "WHERE is_deleted = false AND created_at::date = CURRENT_DATE",
        )

    return {
        "success": True,
        "message": "Dashboard summary retrieved successfully",
        "data": {
            "total_rooms": total_rooms,
            "available_rooms": available_rooms,
            "occupied_rooms": occupied_rooms,
            "today_reservations": reservations,
        },
        "errors": None,
    }
