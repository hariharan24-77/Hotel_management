from fastapi import APIRouter,Depends

from sqlalchemy.ext.asyncio import AsyncSession


from app.database.connection import get_db

from app.schemas.auth import (
    LoginRequest,
    TokenResponse
)

from app.services.auth_service import AuthService
from app.core.dependencies import get_current_user



router=APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)



@router.post(
    "/login",
)
async def login(
    request:LoginRequest,
    db:AsyncSession=Depends(get_db)
):

    service=AuthService(db)


    return await service.login(
        request.email,
        request.password
    )


@router.get("/me")
async def current_user(user=Depends(get_current_user)):
    return {
        "success": True,
        "message": "User retrieved successfully",
        "data": {
            "id": str(user.id),
            "name": user.name,
            "email": user.email,
            "role": user.role.name,
            "role_id": str(user.role_id),
        },
        "errors": None,
    }
