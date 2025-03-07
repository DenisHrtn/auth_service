class BaseRoleException(Exception):
    pass


class RoleAlreadyExists(BaseRoleException):
    pass


class UserAlreadyHasRole(BaseRoleException):
    pass
