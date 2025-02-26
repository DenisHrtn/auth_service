class BaseInteractorException(Exception):
    pass


class UserExistsException(BaseInteractorException):
    pass


class InvalidCodeException(BaseInteractorException):
    pass
