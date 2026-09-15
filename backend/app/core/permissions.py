from fastapi import Depends,HTTPException,status

from app.core.dependencies import get_current_user



def role_required(
    allowed_roles:list
):


    async def check_role(
        user=Depends(get_current_user)
    ):


        user_role=user.role.name


        if user_role not in allowed_roles:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )


        return user


    return check_role