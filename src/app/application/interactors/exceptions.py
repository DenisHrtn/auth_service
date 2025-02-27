class BaseInteractorException(Exception):
    pass


class UserExistsException(BaseInteractorException):
    pass


class InvalidCodeException(BaseInteractorException):
    pass


class UserNotFoundException(BaseInteractorException):
    pass


class UserAlreadyActiveException(BaseInteractorException):
    pass
