from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.database.connection import get_db
from app.models.room_type import RoomType
from app.schemas.room_type import RoomTypeCreate, RoomTypeUpdate

router = APIRouter(prefix="/api/room-types", tags=["Room Types"])


def room_type_data(item: RoomType) -> dict:
    return {
        "id": str(item.id),
        "name": item.name,
        "base_price": float(item.base_price),
        "capacity": item.capacity,
        "bed_type": item.bed_type,
        "description": item.description,
        "is_active": item.is_active,
        "status": "Active" if item.is_active else "Inactive",
    }


@router.get("")
async def list_room_types(
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    result = await db.execute(
        select(RoomType).where(RoomType.is_deleted.is_(False)).order_by(RoomType.name)
    )
    return {
        "success": True,
        "message": "Room types retrieved successfully",
        "data": [room_type_data(item) for item in result.scalars().all()],
        "errors": None,
    }


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_room_type(
    request: RoomTypeCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    name = request.name.strip()
    existing = await db.scalar(
        select(RoomType).where(func.lower(RoomType.name) == name.lower())
    )
    if existing:
        raise HTTPException(status_code=409, detail="Room type already exists")

    item = RoomType(
        name=name,
        base_price=request.base_price,
        capacity=request.capacity,
        bed_type=request.bed_type.strip(),
        description=request.description.strip() if request.description else None,
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return {
        "success": True,
        "message": "Room type created successfully",
        "data": room_type_data(item),
        "errors": None,
    }


@router.get("/{room_type_id}")
async def get_room_type(
    room_type_id: str,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    item = await db.scalar(
        select(RoomType).where(
            RoomType.id == room_type_id,
            RoomType.is_deleted.is_(False),
        )
    )
    if not item:
        raise HTTPException(status_code=404, detail="Room type not found")
    return {
        "success": True,
        "message": "Room type retrieved successfully",
        "data": room_type_data(item),
        "errors": None,
    }


@router.put("/{room_type_id}")
async def update_room_type(
    room_type_id: str,
    request: RoomTypeUpdate,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    item = await db.scalar(
        select(RoomType).where(
            RoomType.id == room_type_id,
            RoomType.is_deleted.is_(False),
        )
    )
    if not item:
        raise HTTPException(status_code=404, detail="Room type not found")

    name = request.name.strip()
    duplicate = await db.scalar(
        select(RoomType).where(
            func.lower(RoomType.name) == name.lower(),
            RoomType.id != room_type_id,
            RoomType.is_deleted.is_(False),
        )
    )
    if duplicate:
        raise HTTPException(status_code=409, detail="Room type name already exists")

    item.name = name
    item.base_price = request.base_price
    item.capacity = request.capacity
    item.bed_type = request.bed_type.strip()
    item.description = request.description.strip() if request.description else None
    item.is_active = request.is_active
    await db.commit()
    await db.refresh(item)
    return {
        "success": True,
        "message": "Room type updated successfully",
        "data": room_type_data(item),
        "errors": None,
    }
