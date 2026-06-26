

class AppException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class NotFoundException(AppException):
    pass


class AlreadyExistsException(AppException):
    pass


class NotAvailablseException(AppException):
    pass