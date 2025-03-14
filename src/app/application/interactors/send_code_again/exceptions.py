class BaseSendCodeAgainException(Exception):
    pass


class UserNotFoundException(BaseSendCodeAgainException):
    pass


class UserAlreadyActiveException(BaseSendCodeAgainException):
    pass
