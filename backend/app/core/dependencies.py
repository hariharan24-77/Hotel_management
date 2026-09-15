<<<<<<< HEAD
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import decode_access_token
from app.models.user import User, RoleEnum

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None or not user.is_active:
        raise credentials_exception
    return user


def require_role(*allowed_roles: RoleEnum):
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )
        return current_user

    return role_checker
=======
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
>>>>>>> sakthi
