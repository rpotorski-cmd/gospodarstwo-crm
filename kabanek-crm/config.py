import os

SECRET_KEY = os.getenv("SECRET_KEY", "kabanek-crm-secret-key-change-in-production-2024")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480  # 8 hours
DATABASE_URL = "sqlite:///./kabanek_crm.db"

# Roles
ROLE_ADMIN = "admin"
ROLE_MANAGER = "manager"
ROLE_WORKER = "pracownik"

ROLES = [ROLE_ADMIN, ROLE_MANAGER, ROLE_WORKER]

# Permissions matrix
PERMISSIONS = {
    ROLE_ADMIN: {
        "users": ["create", "read", "update", "delete"],
        "clients": ["create", "read", "update", "delete"],
        "cycles": ["create", "read", "update", "delete"],
        "feed": ["create", "read", "update", "delete"],
        "finance": ["create", "read", "update", "delete"],
        "dashboard": ["read"],
        "reports": ["read", "export"],
    },
    ROLE_MANAGER: {
        "users": [],
        "clients": ["create", "read", "update"],
        "cycles": ["create", "read", "update"],
        "feed": ["create", "read", "update"],
        "finance": ["create", "read", "update"],
        "dashboard": ["read"],
        "reports": ["read", "export"],
    },
    ROLE_WORKER: {
        "users": [],
        "clients": ["read"],
        "cycles": ["create", "read"],
        "feed": ["read"],
        "finance": ["read"],
        "dashboard": ["read"],
        "reports": ["read"],
    },
}


def has_permission(role: str, resource: str, action: str) -> bool:
    if role not in PERMISSIONS:
        return False
    resource_perms = PERMISSIONS[role].get(resource, [])
    return action in resource_perms
