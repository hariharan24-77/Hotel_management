from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.dependencies import get_current_user
from app.core.security import hash_password
from app.database.connection import get_db
from app.models.role import Role
from app.models.user import User
from app.schemas.staff import StaffCreate, StaffUpdate


router = APIRouter(prefix="/api/staff", tags=["Staff"])


def staff_data(user: User) -> dict:
    return {
        "id": str(user.id),
        "name": user.name,
        "username": user.username,
        "email": user.email,
        "role": user.role.name,
        "role_id": str(user.role_id),
        "is_active": user.is_active,
        "status": "Active" if user.is_active else "Inactive",
    }


@router.get("")
async def list_staff(
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    result = await db.execute(
        select(User)
        .options(selectinload(User.role))
        .where(User.is_deleted.is_(False))
        .order_by(User.created_at.desc())
    )
    return {
        "success": True,
        "message": "Staff retrieved successfully",
        "data": [staff_data(user) for user in result.scalars().all()],
        "errors": None,
    }


@router.get("/{staff_id}")
async def get_staff(
    staff_id: str,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    user = await db.scalar(
        select(User)
        .options(selectinload(User.role))
        .where(User.id == staff_id, User.is_deleted.is_(False))
    )
    if not user:
        raise HTTPException(status_code=404, detail="Staff account not found")
    return {"success": True, "message": "Staff retrieved successfully", "data": staff_data(user), "errors": None}


@router.put("/{staff_id}")
async def update_staff(
    staff_id: str,
    request: StaffUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    user = await db.scalar(
        select(User).options(selectinload(User.role)).where(
            User.id == staff_id, User.is_deleted.is_(False)
        )
    )
    if not user:
        raise HTTPException(status_code=404, detail="Staff account not found")

    duplicate = await db.scalar(
        select(User).where(
            or_(User.email == request.email, User.username == request.username),
            User.id != staff_id,
        )
    )
    if duplicate:
        raise HTTPException(status_code=409, detail="Email or username already exists")

    role = await db.scalar(select(Role).where(
        Role.id == request.role_id,
        Role.is_active.is_(True),
        Role.is_deleted.is_(False),
    ))
    if not role:
        raise HTTPException(status_code=400, detail="Invalid role")

    user.name = request.name.strip()
    user.email = request.email
    user.username = request.username.strip()
    user.role_id = role.id
    user.is_active = request.is_active
    user.updated_by = str(current_user.id)
    await db.commit()
    await db.refresh(user)
    user.role = role
    return {"success": True, "message": "Staff updated successfully", "data": staff_data(user), "errors": None}


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_staff(
    request: StaffCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    duplicate = await db.scalar(
        select(User).where(or_(User.email == request.email, User.username == request.username))
    )
    if duplicate:
        raise HTTPException(status_code=409, detail="Email or username already exists")

    role = await db.scalar(
        select(Role).where(
            Role.id == request.role_id,
            Role.is_active.is_(True),
            Role.is_deleted.is_(False),
        )
    )
    if not role:
        raise HTTPException(status_code=400, detail="Invalid role")

    user = User(
        name=request.name.strip(),
        email=request.email,
        username=request.username.strip(),
        password=hash_password(request.password),
        role_id=role.id,
        created_by=str(current_user.id),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {
        "success": True,
        "message": "Staff created successfully",
        "data": {"id": str(user.id)},
        "errors": None,
    }
