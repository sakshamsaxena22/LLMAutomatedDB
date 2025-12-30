from enum import Enum


class Role(str, Enum):
    viewer = "viewer"
    analyst = "analyst"
    admin = "admin"


ROLE_PERMISSIONS = {
    Role.viewer: {"find"},
    Role.analyst: {"find", "aggregate"},
    Role.admin: {"find", "aggregate", "insert", "update"},
}


def check_permission(role: Role, operation: str):
    allowed = ROLE_PERMISSIONS.get(role, set())
    if operation not in allowed:
        raise PermissionError(
            f"Role '{role}' not allowed to perform '{operation}'"
        )
