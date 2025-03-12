class BaseRoleException(Exception):
    pass


class RoleAlreadyExists(BaseRoleException):
    pass


class RoleNotFound(BaseRoleException):
    pass


class UserAlreadyHasRole(BaseRoleException):
    pass
