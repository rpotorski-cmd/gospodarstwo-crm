import os

SECRET_KEY = os.getenv("SECRET_KEY", "receptury-crm-secret-2024-change-in-prod")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480

ROLE_ADMIN = "admin"
ROLE_USER = "user"
ROLE_VIEWER = "viewer"
ROLES = [ROLE_ADMIN, ROLE_USER, ROLE_VIEWER]

MAX_USERS = 4  # admin + 3 others

# Permissions: admin=full, user=edit recipes+prices, viewer=read-only
MODULE_PERMS = {
    "materials":   {ROLE_ADMIN: "rw", ROLE_USER: "rw", ROLE_VIEWER: "r"},
    "recipes":     {ROLE_ADMIN: "rw", ROLE_USER: "rw", ROLE_VIEWER: "r"},
    "norms":       {ROLE_ADMIN: "rw", ROLE_USER: "r",  ROLE_VIEWER: "r"},
    "production":  {ROLE_ADMIN: "rw", ROLE_USER: "r",  ROLE_VIEWER: "r"},
    "users":       {ROLE_ADMIN: "rw", ROLE_USER: "n",  ROLE_VIEWER: "n"},
    "audit":       {ROLE_ADMIN: "rw", ROLE_USER: "n",  ROLE_VIEWER: "n"},
}

def can_read(role, module):
    p = MODULE_PERMS.get(module, {}).get(role, "n")
    return p in ("r", "rw")

def can_write(role, module):
    p = MODULE_PERMS.get(module, {}).get(role, "n")
    return p == "rw"
