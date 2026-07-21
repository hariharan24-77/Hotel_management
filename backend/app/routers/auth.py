from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, RoleEnum
from app.schemas.auth import UserCreate, UserOut, LoginRequest, Token
from app.core.security import hash_password, verify_password, create_access_token
from app.core.dependencies import get_current_user, require_role

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.admin)),
):
    """Only an authenticated admin can create new staff accounts."""
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

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


@router.post("/login", response_model=Token)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is inactive")

    token = create_access_token(data={"sub": str(user.id), "role": user.role.value})
    return Token(access_token=token, role=user.role)


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


# ---- Example role-protected endpoints ----

@router.get("/admin-only")
def admin_only_route(current_user: User = Depends(require_role(RoleEnum.admin))):
    return {"message": f"Welcome admin {current_user.full_name}"}


@router.get("/management")
def management_route(
    current_user: User = Depends(require_role(RoleEnum.admin, RoleEnum.manager))
):
    return {"message": f"Welcome {current_user.role.value} {current_user.full_name}"}


@router.get("/front-desk")
def front_desk_route(
    current_user: User = Depends(
        require_role(RoleEnum.receptionist, RoleEnum.manager, RoleEnum.admin)
    )
):
    return {"message": f"Welcome {current_user.role.value} {current_user.full_name}"}


@router.get("/billing")
def billing_route(
    current_user: User = Depends(require_role(RoleEnum.cashier, RoleEnum.admin))
):
    return {"message": f"Welcome {current_user.role.value} {current_user.full_name}"}