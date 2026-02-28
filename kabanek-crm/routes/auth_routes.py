from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from database import get_db
from models import User, ActivityLog
from auth import (
    verify_password, get_password_hash, create_access_token,
    get_current_user, require_role
)
from config import ROLE_ADMIN, ROLES

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginRequest(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str
    role: str = "pracownik"


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    username: str
    full_name: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True


@router.post("/login")
async def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == req.username).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Nieprawidlowy login lub haslo")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Konto jest nieaktywne")

    token = create_access_token(data={"sub": str(user.id), "role": user.role})

    # Log activity
    db.add(ActivityLog(user_id=user.id, action="login", resource="auth", details="Logowanie"))
    db.commit()

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "role": user.role,
        },
    }


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/users", response_model=List[UserResponse])
async def list_users(
    current_user: User = Depends(require_role(ROLE_ADMIN)),
    db: Session = Depends(get_db),
):
    return db.query(User).order_by(User.full_name).all()


@router.post("/users", response_model=UserResponse)
async def create_user(
    req: UserCreate,
    current_user: User = Depends(require_role(ROLE_ADMIN)),
    db: Session = Depends(get_db),
):
    if req.role not in ROLES:
        raise HTTPException(status_code=400, detail=f"Nieprawidlowa rola. Dozwolone: {ROLES}")
    if db.query(User).filter(User.username == req.username).first():
        raise HTTPException(status_code=400, detail="Uzytkownik o tej nazwie juz istnieje")

    user = User(
        username=req.username,
        password_hash=get_password_hash(req.password),
        full_name=req.full_name,
        role=req.role,
    )
    db.add(user)
    db.add(ActivityLog(
        user_id=current_user.id, action="create", resource="users",
        details=f"Utworzono uzytkownika: {req.username} ({req.role})"
    ))
    db.commit()
    db.refresh(user)
    return user


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    req: UserUpdate,
    current_user: User = Depends(require_role(ROLE_ADMIN)),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Uzytkownik nie znaleziony")

    if req.full_name is not None:
        user.full_name = req.full_name
    if req.role is not None:
        if req.role not in ROLES:
            raise HTTPException(status_code=400, detail=f"Nieprawidlowa rola")
        user.role = req.role
    if req.is_active is not None:
        user.is_active = req.is_active
    if req.password is not None:
        user.password_hash = get_password_hash(req.password)

    db.add(ActivityLog(
        user_id=current_user.id, action="update", resource="users",
        resource_id=user_id, details=f"Zaktualizowano uzytkownika: {user.username}"
    ))
    db.commit()
    db.refresh(user)
    return user


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(require_role(ROLE_ADMIN)),
    db: Session = Depends(get_db),
):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Nie mozesz usunac swojego konta")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Uzytkownik nie znaleziony")

    user.is_active = False  # Soft delete
    db.add(ActivityLog(
        user_id=current_user.id, action="delete", resource="users",
        resource_id=user_id, details=f"Dezaktywowano uzytkownika: {user.username}"
    ))
    db.commit()
    return {"message": "Uzytkownik dezaktywowany"}
