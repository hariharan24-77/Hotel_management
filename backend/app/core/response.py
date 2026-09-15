from typing import Any



def success_response(
    message:str,
    data:Any=None
):

    return {

        "success":True,

        "message":message,

        "data":data,

        "error":None

    }