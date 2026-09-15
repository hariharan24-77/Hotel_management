from fastapi import HTTPException,status
from app.core.api_response import success_response

from app.repositories.auth_repository import AuthRepository

from app.core.security import (
    verify_password,
    create_access_token
)



class AuthService:


    def __init__(
        self,
        db
    ):

        self.repository=AuthRepository(db)



    async def login(
        self,
        email,
        password
    ):


        user=await self.repository.get_user_by_email(
            email
        )


        if not user:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )


        valid=verify_password(
            password,
            user.password
        )


        if not valid:

            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )


        token=create_access_token(
            {
                "sub":str(user.id),
                "role_id":str(user.role_id)
            }
        )


        return success_response(
        message="Login successful",
        data={
            "access_token": token,
            "token_type": "bearer",
            "role": user.role.name,
            "role_id": str(user.role_id),
            "user": {
                "id": str(user.id),
                "name": user.name,
                "email": user.email,
                "role": user.role.name,
                "role_id": str(user.role_id)
            }
        }
    )
