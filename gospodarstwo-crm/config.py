import os

SECRET_KEY = os.getenv("SECRET_KEY", "gospodarstwo-crm-secret-2024-change-in-prod")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480
DATABASE_URL = "sqlite:///./gospodarstwo_crm.db"

ROLE_ADMIN = "admin"
ROLE_USER = "user"
ROLE_ZOO = "zoo"
ROLES = [ROLE_ADMIN, ROLE_USER, ROLE_ZOO]

MAX_USERS = 10
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
MAX_FILE_SIZE_MB = 20

# Modules and which roles can read/write
# admin: full access everywhere
# user: read/write tuczarnie + roslinna, no user management
# zoo: read-only tuczarnie (only: komory, szczepienia, pasza, paszarnia, leki, upadki, wazenia)
MODULE_PERMS = {
    # Tuczarnie
    "cycles":      {"read": [ROLE_ADMIN, ROLE_USER, ROLE_ZOO], "write": [ROLE_ADMIN, ROLE_USER]},
    "deaths":      {"read": [ROLE_ADMIN, ROLE_USER, ROLE_ZOO], "write": [ROLE_ADMIN, ROLE_USER, ROLE_ZOO]},
    "meds":        {"read": [ROLE_ADMIN, ROLE_USER, ROLE_ZOO], "write": [ROLE_ADMIN, ROLE_USER, ROLE_ZOO]},
    "weighings":   {"read": [ROLE_ADMIN, ROLE_USER, ROLE_ZOO], "write": [ROLE_ADMIN, ROLE_USER, ROLE_ZOO]},
    "todos":       {"read": [ROLE_ADMIN, ROLE_USER, ROLE_ZOO], "write": [ROLE_ADMIN, ROLE_USER, ROLE_ZOO]},
    "stock":       {"read": [ROLE_ADMIN, ROLE_USER, ROLE_ZOO], "write": [ROLE_ADMIN, ROLE_USER]},
    "feeds":       {"read": [ROLE_ADMIN, ROLE_USER, ROLE_ZOO], "write": [ROLE_ADMIN, ROLE_USER]},
    "paszarnia":   {"read": [ROLE_ADMIN, ROLE_USER, ROLE_ZOO], "write": [ROLE_ADMIN, ROLE_USER]},
    "silosy":      {"read": [ROLE_ADMIN, ROLE_USER, ROLE_ZOO], "write": [ROLE_ADMIN, ROLE_USER]},
    "ubojnie":     {"read": [ROLE_ADMIN, ROLE_USER],           "write": [ROLE_ADMIN, ROLE_USER]},
    # Roslinna
    "ciagniki":    {"read": [ROLE_ADMIN, ROLE_USER],           "write": [ROLE_ADMIN, ROLE_USER]},
    "grunty":      {"read": [ROLE_ADMIN, ROLE_USER],           "write": [ROLE_ADMIN, ROLE_USER]},
    "uprawy":      {"read": [ROLE_ADMIN, ROLE_USER],           "write": [ROLE_ADMIN, ROLE_USER]},
    "nawozy":      {"read": [ROLE_ADMIN, ROLE_USER],           "write": [ROLE_ADMIN, ROLE_USER]},
    "opryski":     {"read": [ROLE_ADMIN, ROLE_USER],           "write": [ROLE_ADMIN, ROLE_USER]},
    "paliwa":      {"read": [ROLE_ADMIN, ROLE_USER],           "write": [ROLE_ADMIN, ROLE_USER]},
    "rdostawy":    {"read": [ROLE_ADMIN, ROLE_USER],           "write": [ROLE_ADMIN, ROLE_USER]},
    "zakupy":      {"read": [ROLE_ADMIN, ROLE_USER],           "write": [ROLE_ADMIN, ROLE_USER]},
    "biogaz":      {"read": [ROLE_ADMIN, ROLE_USER],           "write": [ROLE_ADMIN, ROLE_USER]},
    "dokumenty":   {"read": [ROLE_ADMIN, ROLE_USER],           "write": [ROLE_ADMIN]},
    "akcyza":      {"read": [ROLE_ADMIN, ROLE_USER],           "write": [ROLE_ADMIN]},
    # System
    "audit":       {"read": [ROLE_ADMIN],                      "write": [ROLE_ADMIN]},
    "users":       {"read": [ROLE_ADMIN],                      "write": [ROLE_ADMIN]},
}


def can_read(role, module):
    perms = MODULE_PERMS.get(module)
    return perms and role in perms.get("read", [])


def can_write(role, module):
    perms = MODULE_PERMS.get(module)
    return perms and role in perms.get("write", [])
