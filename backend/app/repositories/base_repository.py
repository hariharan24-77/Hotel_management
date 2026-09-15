from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select



class BaseRepository:


    def __init__(
        self,
        db:AsyncSession,
        model
    ):

        self.db=db

        self.model=model



    async def get_by_id(
        self,
        id
    ):

        result=await self.db.execute(

            select(self.model)
            .where(
                self.model.id==id,
                self.model.is_deleted==False
            )

        )


        return result.scalar_one_or_none()



    async def create(
        self,
        obj
    ):

        self.db.add(obj)

        await self.db.commit()

        await self.db.refresh(obj)

        return obj



    async def soft_delete(
        self,
        obj
    ):

        obj.is_deleted=True

        await self.db.commit()

        return True