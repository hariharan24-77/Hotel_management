from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select

from app.models.user import User

from app.models.role import Role



class UserRepository:


    def __init__(
        self,
        db:AsyncSession
    ):

        self.db=db



    async def get_role_by_name(
        self,
        name:str
    ):


        result=await self.db.execute(
            select(Role)
            .where(
                Role.name==name
            )
        )


        return result.scalar_one_or_none()



    async def get_user_by_email(
        self,
        email:str
    ):


        result=await self.db.execute(
            select(User)
            .where(
                User.email==email
            )
        )


        return result.scalar_one_or_none()



    async def create_user(
        self,
        user:User
    ):

        self.db.add(user)

        await self.db.commit()

        await self.db.refresh(user)

        return user