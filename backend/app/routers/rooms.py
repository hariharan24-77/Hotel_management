from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.dependencies import get_current_user
from app.database.connection import get_db
from app.models.room import Room
from app.models.room_type import RoomType
from app.schemas.room import RoomCreate, RoomUpdate

router = APIRouter(prefix="/api/rooms", tags=["Rooms"])


def room_data(room: Room) -> dict:
    return {
        "id": str(room.id),
        "room_number": room.room_number,
        "floor": room.floor,
        "room_type_id": str(room.room_type_id),
        "room_type": room.room_type.name,
        "status": room.status,
        "is_active": room.is_active,
    }


@router.get("")
async def list_rooms(
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    result = await db.execute(
        select(Room)
        .options(selectinload(Room.room_type))
        .where(Room.is_deleted.is_(False))
        .order_by(Room.room_number)
    )
    return {
        "success": True,
        "message": "Rooms retrieved successfully",
        "data": [room_data(room) for room in result.scalars().all()],
        "errors": None,
    }


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_room(
    request: RoomCreate,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    number = request.room_number.strip()
    if await db.scalar(
        select(Room).where(Room.room_number == number, Room.is_deleted.is_(False))
    ):
        raise HTTPException(status_code=409, detail="Room number already exists")

    room_type = await db.scalar(
        select(RoomType).where(
            RoomType.id == request.room_type_id,
            RoomType.is_active.is_(True),
            RoomType.is_deleted.is_(False),
        )
    )
    if not room_type:
        raise HTTPException(status_code=400, detail="Invalid or inactive room type")

    room = Room(
        room_number=number,
        floor=request.floor,
        room_type_id=room_type.id,
        status="Available",
    )
    room.room_type = room_type
    db.add(room)
    await db.commit()
    await db.refresh(room)
    return {
        "success": True,
        "message": "Room created successfully",
        "data": room_data(room),
        "errors": None,
    }


@router.get("/{room_id}")
async def get_room(
    room_id: str, db: AsyncSession = Depends(get_db), _user=Depends(get_current_user)
):
    room = await db.scalar(
        select(Room)
        .options(selectinload(Room.room_type))
        .where(Room.id == room_id, Room.is_deleted.is_(False))
    )
    if not room:
        raise HTTPException(404, "Room not found")
    return {
        "success": True,
        "message": "Room retrieved successfully",
        "data": room_data(room),
        "errors": None,
    }


@router.put("/{room_id}")
async def update_room(
    room_id: str,
    request: RoomUpdate,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    room = await db.scalar(
        select(Room)
        .options(selectinload(Room.room_type))
        .where(Room.id == room_id, Room.is_deleted.is_(False))
    )
    if not room:
        raise HTTPException(404, "Room not found")
    duplicate = await db.scalar(
        select(Room).where(
            Room.room_number == request.room_number.strip(),
            Room.id != room_id,
            Room.is_deleted.is_(False),
        )
    )
    room_type = await db.scalar(
        select(RoomType).where(
            RoomType.id == request.room_type_id,
            RoomType.is_deleted.is_(False),
            RoomType.is_active.is_(True),
        )
    )
    if duplicate:
        raise HTTPException(409, "Room number already exists")
    if not room_type:
        raise HTTPException(400, "Invalid room type")
    if room.status == "Occupied" and request.status != "Occupied":
        raise HTTPException(
            409, "An occupied room must be checked out before its status can change"
        )
    if room.status != "Occupied" and request.status == "Occupied":
        raise HTTPException(409, "Use guest check-in to mark a room as occupied")
    room.room_number = request.room_number.strip()
    room.floor = request.floor
    room.room_type_id = room_type.id
    room.room_type = room_type
    room.status = request.status
    room.is_active = request.status not in ("Maintenance", "Inactive")
    await db.commit()
    await db.refresh(room)
    return {
        "success": True,
        "message": "Room updated successfully",
        "data": room_data(room),
        "errors": None,
    }
