from app.exceptions.custom import AppException



class UserNotFoundException(
    AppException
):

    def __init__(self):

        super().__init__(
            message="User not found",
            error_code="USER_NOT_FOUND",
            status_code=404
        )



class EmailAlreadyExistsException(
    AppException
):

    def __init__(self):

        super().__init__(
            message="Email already exists",
            error_code="EMAIL_EXISTS",
            status_code=400
        )



class InvalidCredentialsException(
    AppException
):

    def __init__(self):

        super().__init__(
            message="Invalid email or password",
            error_code="INVALID_CREDENTIALS",
            status_code=401
        )