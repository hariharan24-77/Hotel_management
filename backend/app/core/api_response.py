from fastapi.responses import JSONResponse


def success_response(
    message: str,
    data=None,
    status_code: int = 200
):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "message": message,
            "data": data,
            "errors": None
        }
    )


def error_response(
    message: str,
    errors=None,
    status_code: int = 400
):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "data": None,
            "errors": errors
        }
    )