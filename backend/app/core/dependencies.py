from fastapi import Depends,HTTPException,status

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.security import decode_access_token

from app.database.connection import get_db

from app.models.user import User



oauth2_scheme=OAuth2PasswordBearer(
    tokenUrl="/api/auth/login"
)



async def get_current_user(
    token:str=Depends(oauth2_scheme),
    db:AsyncSession=Depends(get_db)
):

    payload=decode_access_token(
        token
    )


    if not payload:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


    user_id=payload.get(
        "sub"
    )


    result=await db.execute(
        select(User).options(selectinload(User.role))
        .where(
            User.id==user_id
        )
    )


    user=result.scalar_one_or_none()


    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )


    return user
