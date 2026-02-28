from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from database import get_db
from models import Client, ClientAssignment, ActivityLog, User
from auth import get_current_user, require_permission
from config import ROLE_ADMIN, ROLE_MANAGER, ROLE_WORKER

router = APIRouter(prefix="/api/clients", tags=["clients"])


class ClientCreate(BaseModel):
    name: str
    kolczyk: str = ""
    feeds: str = ""


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    cycles: Optional[int] = None
    pigs: Optional[int] = None
    sold: Optional[int] = None
    profit: Optional[float] = None
    mortality: Optional[float] = None
    fcr: Optional[float] = None
    deaths: Optional[int] = None
    kolczyk: Optional[str] = None
    profit_per_pig: Optional[float] = None
    feeds: Optional[str] = None
    is_active: Optional[bool] = None


class ClientResponse(BaseModel):
    id: int
    name: str
    cycles: int
    pigs: int
    sold: int
    profit: float
    mortality: float
    fcr: float
    deaths: int
    kolczyk: str
    profit_per_pig: float
    feeds: str
    is_active: bool

    class Config:
        from_attributes = True


class AssignClientRequest(BaseModel):
    user_id: int
    client_id: int


@router.get("", response_model=List[ClientResponse])
async def list_clients(
    search: Optional[str] = None,
    kolczyk: Optional[str] = None,
    preset: Optional[str] = None,
    limit: int = Query(default=100, le=500),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(Client).filter(Client.is_active == True)

    # Workers can only see assigned clients
    if current_user.role == ROLE_WORKER:
        assigned_ids = [
            a.client_id for a in
            db.query(ClientAssignment).filter(ClientAssignment.user_id == current_user.id).all()
        ]
        if assigned_ids:
            query = query.filter(Client.id.in_(assigned_ids))
        else:
            return []

    if search:
        query = query.filter(Client.name.ilike(f"%{search}%"))
    if kolczyk:
        query = query.filter(Client.kolczyk.ilike(f"%{kolczyk}%"))

    # Presets
    if preset == "topProfit":
        query = query.filter(Client.profit > 0).order_by(Client.profit.desc())
    elif preset == "botProfit":
        query = query.order_by(Client.profit.asc())
    elif preset == "bestFcr":
        query = query.filter(Client.fcr > 0).order_by(Client.fcr.asc())
    elif preset == "worstFcr":
        query = query.filter(Client.fcr > 0).order_by(Client.fcr.desc())
    elif preset == "lowMort":
        query = query.order_by(Client.mortality.asc())
    elif preset == "highMort":
        query = query.order_by(Client.mortality.desc())
    else:
        query = query.order_by(Client.pigs.desc())

    return query.limit(limit).all()


@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(
    client_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Klient nie znaleziony")

    # Check worker access
    if current_user.role == ROLE_WORKER:
        assignment = db.query(ClientAssignment).filter(
            ClientAssignment.user_id == current_user.id,
            ClientAssignment.client_id == client_id,
        ).first()
        if not assignment:
            raise HTTPException(status_code=403, detail="Brak dostepu do tego klienta")

    return client


@router.post("", response_model=ClientResponse)
async def create_client(
    req: ClientCreate,
    current_user: User = Depends(require_permission("clients", "create")),
    db: Session = Depends(get_db),
):
    client = Client(name=req.name, kolczyk=req.kolczyk, feeds=req.feeds)
    db.add(client)
    db.add(ActivityLog(
        user_id=current_user.id, action="create", resource="clients",
        details=f"Dodano klienta: {req.name}"
    ))
    db.commit()
    db.refresh(client)
    return client


@router.put("/{client_id}", response_model=ClientResponse)
async def update_client(
    client_id: int,
    req: ClientUpdate,
    current_user: User = Depends(require_permission("clients", "update")),
    db: Session = Depends(get_db),
):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Klient nie znaleziony")

    for field, value in req.dict(exclude_unset=True).items():
        setattr(client, field, value)

    db.add(ActivityLog(
        user_id=current_user.id, action="update", resource="clients",
        resource_id=client_id, details=f"Zaktualizowano klienta: {client.name}"
    ))
    db.commit()
    db.refresh(client)
    return client


@router.delete("/{client_id}")
async def delete_client(
    client_id: int,
    current_user: User = Depends(require_permission("clients", "delete")),
    db: Session = Depends(get_db),
):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Klient nie znaleziony")

    client.is_active = False
    db.add(ActivityLog(
        user_id=current_user.id, action="delete", resource="clients",
        resource_id=client_id, details=f"Usunięto klienta: {client.name}"
    ))
    db.commit()
    return {"message": "Klient usuniety"}


# --- Client Assignments (admin only) ---

@router.post("/assign")
async def assign_client(
    req: AssignClientRequest,
    current_user: User = Depends(require_permission("users", "update")),
    db: Session = Depends(get_db),
):
    existing = db.query(ClientAssignment).filter(
        ClientAssignment.user_id == req.user_id,
        ClientAssignment.client_id == req.client_id,
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Klient juz przypisany do tego uzytkownika")

    assignment = ClientAssignment(user_id=req.user_id, client_id=req.client_id)
    db.add(assignment)
    db.commit()
    return {"message": "Klient przypisany"}


@router.delete("/assign/{assignment_id}")
async def unassign_client(
    assignment_id: int,
    current_user: User = Depends(require_permission("users", "update")),
    db: Session = Depends(get_db),
):
    assignment = db.query(ClientAssignment).filter(ClientAssignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Przypisanie nie znalezione")
    db.delete(assignment)
    db.commit()
    return {"message": "Przypisanie usunięte"}


@router.get("/assignments/{user_id}")
async def get_user_assignments(
    user_id: int,
    current_user: User = Depends(require_permission("users", "read")),
    db: Session = Depends(get_db),
):
    assignments = db.query(ClientAssignment).filter(ClientAssignment.user_id == user_id).all()
    result = []
    for a in assignments:
        client = db.query(Client).filter(Client.id == a.client_id).first()
        if client:
            result.append({"assignment_id": a.id, "client_id": client.id, "client_name": client.name})
    return result
