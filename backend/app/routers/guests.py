from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.database.connection import get_db
from app.models.guest import Guest
from app.schemas.guest import GuestCreate, GuestUpdate

router = APIRouter(prefix="/api/guests", tags=["Guests"])


def guest_data(guest: Guest) -> dict:
    return {
        "id": str(guest.id),
        "name": guest.name,
        "phone": guest.phone,
        "email": guest.email,
        "gender": guest.gender,
        "dob": guest.dob.isoformat(),
        "address": guest.address,
        "id_proof_type": guest.id_proof_type,
        "id_proof_number": guest.id_proof_number,
        "id_proof": f"{guest.id_proof_type} - {guest.id_proof_number}",
    }


@router.get("")
async def list_guests(
    db: AsyncSession = Depends(get_db), _user=Depends(get_current_user)
):
    result = await db.execute(
        select(Guest).where(Guest.is_deleted.is_(False)).order_by(Guest.name)
    )
    return {
        "success": True,
        "message": "Guests retrieved successfully",
        "data": [guest_data(item) for item in result.scalars().all()],
        "errors": None,
    }


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_guest(
    request: GuestCreate,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    proof = request.id_proof_number.strip()
    if await db.scalar(
        select(Guest).where(Guest.id_proof_number == proof, Guest.is_deleted.is_(False))
    ):
        raise HTTPException(status_code=409, detail="ID proof number already exists")
    guest = Guest(
        **request.model_dump(exclude={"id_proof_number"}), id_proof_number=proof
    )
    db.add(guest)
    await db.commit()
    await db.refresh(guest)
    return {
        "success": True,
        "message": "Guest created successfully",
        "data": guest_data(guest),
        "errors": None,
    }


@router.get("/{guest_id}")
async def get_guest(
    guest_id: str, db: AsyncSession = Depends(get_db), _user=Depends(get_current_user)
):
    guest = await db.scalar(
        select(Guest).where(Guest.id == guest_id, Guest.is_deleted.is_(False))
    )
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    return {
        "success": True,
        "message": "Guest retrieved successfully",
        "data": guest_data(guest),
        "errors": None,
    }


@router.put("/{guest_id}")
async def update_guest(
    guest_id: str,
    request: GuestUpdate,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    guest = await db.scalar(
        select(Guest).where(Guest.id == guest_id, Guest.is_deleted.is_(False))
    )
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    duplicate = await db.scalar(
        select(Guest).where(
            Guest.id_proof_number == request.id_proof_number.strip(),
            Guest.id != guest_id,
            Guest.is_deleted.is_(False),
        )
    )
    if duplicate:
        raise HTTPException(status_code=409, detail="ID proof number already exists")
    for field, value in request.model_dump().items():
        setattr(guest, field, value.strip() if isinstance(value, str) else value)
    await db.commit()
    await db.refresh(guest)
    return {
        "success": True,
        "message": "Guest updated successfully",
        "data": guest_data(guest),
        "errors": None,
    }


@router.delete("/{guest_id}")
async def delete_guest(
    guest_id: str, db: AsyncSession = Depends(get_db), _user=Depends(get_current_user)
):
    guest = await db.scalar(
        select(Guest).where(Guest.id == guest_id, Guest.is_deleted.is_(False))
    )
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    guest.is_deleted = True
    await db.commit()
    return {
        "success": True,
        "message": "Guest deleted successfully",
        "data": None,
        "errors": None,
    }
