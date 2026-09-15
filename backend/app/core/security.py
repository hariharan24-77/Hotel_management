<<<<<<< HEAD
import uuid
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token_value() -> str:
    """Random opaque string stored in DB — not a JWT, just a secure random token."""
    return uuid.uuid4().hex + uuid.uuid4().hex


def decode_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "access":
            return None
        return payload
    except JWTError:
=======
from datetime import datetime,timedelta,timezone

from jose import jwt

from passlib.context import CryptContext

from app.core.config import settings


password_context=CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password:str):

    return password_context.hash(password)



def verify_password(
    plain_password,
    hashed_password
):

    return password_context.verify(
        plain_password,
        hashed_password
    )



def create_access_token(data:dict):

    payload=data.copy()

    expire=datetime.now(timezone.utc)+timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload.update(
        {
            "exp":expire
        }
    )


    token=jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


    return token



def decode_access_token(token:str):

    try:

        payload=jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[
                settings.ALGORITHM
            ]
        )

        return payload


    except Exception:

>>>>>>> sakthi
        return None