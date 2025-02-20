class BaseUserException(Exception):
    pass


class UserWithInvalidPasswordException(BaseUserException):
    pass


class UserWithoutEmailException(BaseUserException):
    pass


class UserWithoutPasswordException(BaseUserException):
    pass
