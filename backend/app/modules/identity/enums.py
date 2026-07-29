"""Identity enums. Roles are an enum, never string literals."""

from enum import StrEnum


class UserRole(StrEnum):
    ADMIN = "admin"
    RECRUITER = "recruiter"
    HIRING_MANAGER = "hiring_manager"
