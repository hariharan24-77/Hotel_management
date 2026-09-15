import os
import uuid


from fastapi import UploadFile,HTTPException


from app.core.file_config import (
    ALLOWED_TYPES,
    MAX_FILE_SIZE
)



class FileService:



    async def save_file(
        self,
        file:UploadFile,
        folder:str="images"
    ):


        if file.content_type not in ALLOWED_TYPES:

            raise HTTPException(
                400,
                "File type not allowed"
            )


        content=await file.read()



        if len(content)>MAX_FILE_SIZE:

            raise HTTPException(
                400,
                "File size exceeded"
            )



        extension=file.filename.split(".")[-1]


        new_name=f"{uuid.uuid4()}.{extension}"



        path=f"storage/{folder}/{new_name}"



        os.makedirs(
            f"storage/{folder}",
            exist_ok=True
        )



        with open(
            path,
            "wb"
        ) as buffer:

            buffer.write(content)



        return {

            "file_name":file.filename,

            "file_path":path,

            "file_type":file.content_type,

            "file_size":len(content)

        }