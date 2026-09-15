from typing import Generic,TypeVar,Optional

from pydantic import BaseModel


T=TypeVar("T")



class ResponseSchema(
    BaseModel,
    Generic[T]
):

    success:bool

    message:str

    data:Optional[T]=None

    error:Optional[str]=None