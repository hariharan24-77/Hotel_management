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

        return None