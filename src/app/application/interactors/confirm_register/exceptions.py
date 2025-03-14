class BaseConfirmInteractorException(Exception):
    pass


class UserExistsException(BaseConfirmInteractorException):
    pass


class InvalidCodeException(BaseConfirmInteractorException):
    pass


class UserAlreadyActiveException(BaseConfirmInteractorException):
    pass
