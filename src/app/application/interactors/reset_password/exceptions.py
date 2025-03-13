class BasePasswordResetException(Exception):
    pass


class UserNotActive(BasePasswordResetException):
    pass
