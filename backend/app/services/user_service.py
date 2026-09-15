from fastapi import HTTPException

from app.models.user import User

from app.repositories.user_repository import UserRepository

from app.core.security import hash_password



class UserService:


    def __init__(
        self,
        db
    ):

        self.repository=UserRepository(db)



    async def create_master_admin(
        self,
        data
    ):


        existing=await self.repository.get_user_by_email(
            data.email
        )


        if existing:

            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )


        role=await self.repository.get_role_by_name(
            "MASTER_ADMIN"
        )


        user=User(

            name=data.name,

            email=data.email,

            password=hash_password(
                data.password
            ),

            role_id=role.id

        )


        return await self.repository.create_user(
            user
        )