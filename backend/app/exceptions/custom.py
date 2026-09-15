class AppException(Exception):

    def __init__(
        self,
        message:str,
        error_code:str,
        status_code:int
    ):

        self.message=message

        self.error_code=error_code

        self.status_code=status_code