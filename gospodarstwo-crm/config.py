import os
import secrets

# SECURITY: SECRET_KEY MUST be set in environment (Railway settings)
# If not set, generate random one (will invalidate tokens on restart - safe default)
SECRET_KEY = os.getenv("SECRET_KEY", "")
if not SECRET_KEY:
    SECRET_KEY = secrets.token_hex(32)
    print("⚠️ SECRET_KEY not set! Generated random key. Set SECRET_KEY in Railway env variables for persistent sessions.")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480

# Railway sets DATABASE_URL automatically when you add PostgreSQL plugin
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./gospodarstwo_crm.db")

ROLE_ADMIN = "admin"
ROLE_USER = "user"
ROLE_ZOO = "zoo"
ROLES = [ROLE_ADMIN, ROLE_USER, ROLE_ZOO]

MAX_USERS = 10

# Use /data/uploads on Railway (volume mount) or local uploads/
UPLOAD_DIR = os.getenv("UPLOAD_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads"))
MAX_FILE_SIZE_MB = 20

MODULE_PERMS = {
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
    "audit":       {"read": [ROLE_ADMIN],                      "write": [ROLE_ADMIN]},
    "users":       {"read": [ROLE_ADMIN],                      "write": [ROLE_ADMIN]},
}


def can_read(role, module):
    perms = MODULE_PERMS.get(module)
    return perms and role in perms.get("read", [])


def can_write(role, module):
    perms = MODULE_PERMS.get(module)
    return perms and role in perms.get("write", [])
