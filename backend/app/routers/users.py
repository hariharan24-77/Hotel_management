from fastapi import APIRouter,Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.connection import get_db

from app.schemas.user import MasterAdminCreate

from app.services.user_service import UserService
from app.models.role import Role
from app.core.dependencies import get_current_user



router=APIRouter(
    prefix="/api/users",
    tags=["Users"]
)


@router.get("/roles")
async def list_roles(
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    result = await db.execute(
        select(Role).where(Role.is_active.is_(True), Role.is_deleted.is_(False)).order_by(Role.name)
    )
    return {
        "success": True,
        "message": "Roles retrieved successfully",
        "data": [
            {"id": str(role.id), "name": role.name}
            for role in result.scalars().all()
        ],
        "errors": None,
    }



@router.post(
    "/create-master-admin"
)
async def create_master_admin(
    request:MasterAdminCreate,
    db:AsyncSession=Depends(get_db)
):

    service=UserService(db)


    user=await service.create_master_admin(
        request
    )


    return {

        "message":
        "Master admin created",

        "user_id":
        str(user.id)

    }
