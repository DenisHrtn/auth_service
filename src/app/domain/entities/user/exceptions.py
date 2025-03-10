class BaseUserException(Exception):
    pass


class InvalidUserPasswordException(BaseUserException):
    pass


class InvalidUserEmailException(BaseUserException):
    pass


class InvalidUserUsernameException(BaseUserException):
    pass
