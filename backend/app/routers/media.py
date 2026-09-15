from fastapi import APIRouter,UploadFile,File,Depends

from sqlalchemy.ext.asyncio import AsyncSession


from app.database.connection import get_db

from app.services.file_service import FileService

from app.core.dependencies import get_current_user



router=APIRouter(

    prefix="/api/media",

    tags=["Media"]

)



@router.post(
    "/upload"
)
async def upload_file(

    file:UploadFile=File(...),

    user=Depends(
        get_current_user
    ),

):


    service=FileService()


    result=await service.save_file(
        file
    )



    return {

        "success":True,

        "message":
        "File uploaded successfully",

        "data":result,

        "error":None

    }