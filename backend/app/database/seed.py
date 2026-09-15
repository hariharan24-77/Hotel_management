from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select

from app.models.role import Role



DEFAULT_ROLES=[
    "MASTER_ADMIN",
    "ADMIN",
    "RECEPTIONIST",
    "ACCOUNTANT",
    "MANAGER"
]



async def seed_roles(
    db:AsyncSession
):

    for role_name in DEFAULT_ROLES:


        result=await db.execute(
            select(Role)
            .where(
                Role.name==role_name
            )
        )


        existing=result.scalar_one_or_none()


        if not existing:

            role=Role(
                name=role_name
            )

            db.add(role)


    await db.commit()