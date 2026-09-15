<<<<<<< HEAD
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db

from app.models.user import User, RoleEnum
from app.models.refresh_token import RefreshToken

from app.schemas.auth import (
    UserCreate,
    UserOut,
    LoginRequest,
    Token,
    RefreshRequest,
    AccessTokenOnly,
    TokenUser,
)

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token_value,
)

from app.core.dependencies import (
    get_current_user,
    require_role,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


# ------------------------------------------------------------------
# Register
# ------------------------------------------------------------------
@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.admin)),
):
    existing = db.query(User).filter(User.email == user_in.email).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    user = User(
        full_name=user_in.full_name,
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        role=user_in.role,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# ------------------------------------------------------------------
# Login
# ------------------------------------------------------------------
@router.post("/login", response_model=Token)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(
        User.email == credentials.email
    ).first()

    if not user or not verify_password(
        credentials.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Account is inactive",
        )

    # Access Token
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "role": user.role.value,
        }
    )

    # Refresh Token
    refresh_token = create_refresh_token_value()

    refresh_expiry = (
        datetime.now(timezone.utc)
        + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )

    db_refresh = RefreshToken(
        token=refresh_token,
        user_id=user.id,
        expires_at=refresh_expiry,
        revoked=False,
    )

    db.add(db_refresh)
    db.commit()

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        user=TokenUser(
            id=user.id,
            full_name=user.full_name,
            role=user.role,
        ),
    )


# ------------------------------------------------------------------
# Refresh Access Token
# ------------------------------------------------------------------
@router.post("/refresh", response_model=AccessTokenOnly)
def refresh_token(
    payload: RefreshRequest,
    db: Session = Depends(get_db),
):
    db_token = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token == payload.refresh_token
        )
        .first()
    )

    if not db_token or db_token.revoked:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
        )

    if db_token.expires_at.replace(
        tzinfo=timezone.utc
    ) < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=401,
            detail="Refresh token expired",
        )

    user = (
        db.query(User)
        .filter(User.id == db_token.user_id)
        .first()
    )

    if not user or not user.is_active:
        raise HTTPException(
            status_code=401,
            detail="User not found or inactive",
        )

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "role": user.role.value,
        }
    )

    return AccessTokenOnly(
        access_token=access_token
    )


# ------------------------------------------------------------------
# Logout
# ------------------------------------------------------------------
@router.post("/logout")
def logout(
    payload: RefreshRequest,
    db: Session = Depends(get_db),
):
    db_token = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token == payload.refresh_token
        )
        .first()
    )

    if db_token:
        db_token.revoked = True
        db.commit()

    return {
        "message": "Logged out successfully"
    }


# ------------------------------------------------------------------
# Current User
# ------------------------------------------------------------------
@router.get("/me", response_model=UserOut)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user


# ------------------------------------------------------------------
# Admin Only
# ------------------------------------------------------------------
@router.get("/admin-only")
def admin_only_route(
    current_user: User = Depends(
        require_role(RoleEnum.admin)
    ),
):
    return {
        "message": f"Welcome admin {current_user.full_name}"
    }


# ------------------------------------------------------------------
# Admin & Manager
# ------------------------------------------------------------------
@router.get("/management")
def management_route(
    current_user: User = Depends(
        require_role(
            RoleEnum.admin,
            RoleEnum.manager,
        )
    ),
):
    return {
        "message": f"Welcome {current_user.role.value} {current_user.full_name}"
    }


# ------------------------------------------------------------------
# Front Desk
# ------------------------------------------------------------------
@router.get("/front-desk")
def front_desk_route(
    current_user: User = Depends(
        require_role(
            RoleEnum.receptionist,
            RoleEnum.manager,
            RoleEnum.admin,
        )
    ),
):
    return {
        "message": f"Welcome {current_user.role.value} {current_user.full_name}"
    }


# ------------------------------------------------------------------
# Billing
# ------------------------------------------------------------------
@router.get("/billing")
def billing_route(
    current_user: User = Depends(
        require_role(
            RoleEnum.cashier,
            RoleEnum.admin,
        )
    ),
):
    return {
        "message": f"Welcome {current_user.role.value} {current_user.full_name}"
    }
=======
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
>>>>>>> sakthi
