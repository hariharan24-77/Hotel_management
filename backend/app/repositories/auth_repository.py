from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.user import User



class AuthRepository:


    def __init__(
        self,
        db:AsyncSession
    ):

        self.db=db



    async def get_user_by_email(
        self,
        email:str
    ):

        result = await self.db.execute(
    select(User)
    .options(selectinload(User.role))
    .where(User.email == email)
)

        user = result.scalar_one_or_none()
        return user