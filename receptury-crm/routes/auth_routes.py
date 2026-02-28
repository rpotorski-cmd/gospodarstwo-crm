from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
from models import User, AuditLog
from auth import verify_password, create_token, hash_password, get_current_user, require_role
from config import ROLE_ADMIN, MAX_USERS
from datetime import datetime

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginReq(BaseModel):
    email: str
    password: str

class UserCreate(BaseModel):
    email: str
    name: str
    password: str
    role: str = "user"

class UserUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


def audit(db, user, area, action):
    db.add(AuditLog(user_name=user.name, email=user.email, area=area, action=action))
    db.commit()


@router.post("/login")
async def login(req: LoginReq, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email, User.is_active == True).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Nieprawidłowy email lub hasło")
    token = create_token({"sub": str(user.id), "role": user.role})
    audit(db, user, "login", "Zalogowano")
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"id": user.id, "email": user.email, "name": user.name, "role": user.role}
    }


@router.get("/me")
async def me(user: User = Depends(get_current_user)):
    return {"id": user.id, "email": user.email, "name": user.name, "role": user.role}


@router.get("/users")
async def list_users(user: User = Depends(require_role(ROLE_ADMIN)), db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": u.id, "email": u.email, "name": u.name, "role": u.role, "is_active": u.is_active} for u in users]


@router.post("/users")
async def create_user(req: UserCreate, user: User = Depends(require_role(ROLE_ADMIN)), db: Session = Depends(get_db)):
    total = db.query(User).filter(User.is_active == True).count()
    if total >= MAX_USERS:
        raise HTTPException(status_code=400, detail=f"Osiągnięto limit {MAX_USERS} użytkowników (admin + 3). Dezaktywuj kogoś aby dodać nowego.")
    if db.query(User).filter(User.email == req.email).first():
        raise HTTPException(status_code=400, detail="Email zajęty")
    new = User(email=req.email, name=req.name, password_hash=hash_password(req.password), role=req.role)
    db.add(new)
    db.commit()
    db.refresh(new)
    audit(db, user, "users", f"Utworzono: {req.name} ({req.role})")
    return {"id": new.id, "email": new.email, "name": new.name, "role": new.role}


@router.put("/users/{uid}")
async def update_user(uid: int, req: UserUpdate, user: User = Depends(require_role(ROLE_ADMIN)), db: Session = Depends(get_db)):
    target = db.query(User).filter(User.id == uid).first()
    if not target:
        raise HTTPException(status_code=404, detail="Nie znaleziono")
    if req.name is not None: target.name = req.name
    if req.role is not None: target.role = req.role
    if req.password is not None: target.password_hash = hash_password(req.password)
    if req.is_active is not None: target.is_active = req.is_active
    db.commit()
    audit(db, user, "users", f"Zaktualizowano: {target.name}")
    return {"ok": True}


@router.delete("/users/{uid}")
async def delete_user(uid: int, user: User = Depends(require_role(ROLE_ADMIN)), db: Session = Depends(get_db)):
    target = db.query(User).filter(User.id == uid).first()
    if not target:
        raise HTTPException(status_code=404, detail="Nie znaleziono")
    target.is_active = False
    db.commit()
    audit(db, user, "users", f"Dezaktywowano: {target.name}")
    return {"ok": True}


@router.get("/audit")
async def get_audit(limit: int = 200, user: User = Depends(require_role(ROLE_ADMIN)), db: Session = Depends(get_db)):
    logs = db.query(AuditLog).order_by(AuditLog.id.desc()).limit(limit).all()
    return [{"ts": str(l.ts), "user": l.user_name, "email": l.email, "area": l.area, "action": l.action} for l in logs]
