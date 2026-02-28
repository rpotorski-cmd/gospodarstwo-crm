import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from database import get_db
from models import User, Material, Recipe, Norm, Production, AuditLog
from auth import get_current_user
from config import can_read, can_write

router = APIRouter(prefix="/api", tags=["data"])


def audit(db, user, area, action):
    db.add(AuditLog(user_name=user.name, email=user.email, area=area, action=action))
    db.commit()


def require_read(user, module):
    if not can_read(user.role, module):
        raise HTTPException(status_code=403, detail="Brak uprawnień do odczytu")

def require_write(user, module):
    if not can_write(user.role, module):
        raise HTTPException(status_code=403, detail="Brak uprawnień do zapisu")


# ══════════════════════════════════════════════════════════════════════════════
# MATERIALS (surowce)
# ══════════════════════════════════════════════════════════════════════════════

def mat_to_dict(m):
    return {
        "id": m.id, "sortOrder": m.sort_order, "n": m.name, "c": m.price,
        "b": m.protein, "NE": m.ne, "Ly": m.lys, "Me": m.met,
        "Th": m.thr, "Tr": m.trp, "W": m.fiber, "Ca": m.calcium, "P": m.phosphorus
    }


@router.get("/materials")
async def get_materials(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    require_read(user, "materials")
    mats = db.query(Material).order_by(Material.sort_order).all()
    return [mat_to_dict(m) for m in mats]


class MaterialUpdate(BaseModel):
    n: Optional[str] = None
    c: Optional[float] = None
    b: Optional[float] = None
    NE: Optional[float] = None
    Ly: Optional[float] = None
    Me: Optional[float] = None
    Th: Optional[float] = None
    Tr: Optional[float] = None
    W: Optional[float] = None
    Ca: Optional[float] = None
    P: Optional[float] = None


@router.put("/materials/{mid}")
async def update_material(mid: int, req: MaterialUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    require_write(user, "materials")
    m = db.query(Material).filter(Material.id == mid).first()
    if not m:
        raise HTTPException(status_code=404, detail="Nie znaleziono")
    field_map = {"n": "name", "c": "price", "b": "protein", "NE": "ne",
                 "Ly": "lys", "Me": "met", "Th": "thr", "Tr": "trp",
                 "W": "fiber", "Ca": "calcium", "P": "phosphorus"}
    changes = []
    for js_key, db_key in field_map.items():
        val = getattr(req, js_key, None)
        if val is not None:
            old = getattr(m, db_key)
            setattr(m, db_key, val)
            changes.append(f"{js_key}: {old}→{val}")
    db.commit()
    if changes:
        audit(db, user, "materials", f"Zmieniono {m.name}: {', '.join(changes)}")
    return mat_to_dict(m)


class MaterialCreate(BaseModel):
    n: str
    c: float = 0
    b: float = 0
    NE: float = 0
    Ly: float = 0
    Me: float = 0
    Th: float = 0
    Tr: float = 0
    W: float = 0
    Ca: float = 0
    P: float = 0


@router.post("/materials")
async def create_material(req: MaterialCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    require_write(user, "materials")
    max_order = db.query(Material).count()
    m = Material(
        sort_order=max_order, name=req.n, price=req.c, protein=req.b, ne=req.NE,
        lys=req.Ly, met=req.Me, thr=req.Th, trp=req.Tr,
        fiber=req.W, calcium=req.Ca, phosphorus=req.P
    )
    db.add(m)
    db.commit()
    db.refresh(m)
    # Extend all recipes with 0 for new material
    for recipe in db.query(Recipe).all():
        shares = json.loads(recipe.shares)
        shares.append(0)
        recipe.shares = json.dumps(shares)
    db.commit()
    audit(db, user, "materials", f"Dodano surowiec: {req.n}")
    return mat_to_dict(m)


@router.delete("/materials/{mid}")
async def delete_material(mid: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    require_write(user, "materials")
    m = db.query(Material).filter(Material.id == mid).first()
    if not m:
        raise HTTPException(status_code=404, detail="Nie znaleziono")
    idx = m.sort_order
    name = m.name
    db.delete(m)
    # Remove from all recipes and reindex
    for recipe in db.query(Recipe).all():
        shares = json.loads(recipe.shares)
        if idx < len(shares):
            shares.pop(idx)
        recipe.shares = json.dumps(shares)
    # Reindex remaining materials
    remaining = db.query(Material).order_by(Material.sort_order).all()
    for i, mat in enumerate(remaining):
        mat.sort_order = i
    db.commit()
    audit(db, user, "materials", f"Usunięto surowiec: {name}")
    return {"ok": True}


# ══════════════════════════════════════════════════════════════════════════════
# RECIPES
# ══════════════════════════════════════════════════════════════════════════════

@router.get("/recipes")
async def get_recipes(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    require_read(user, "recipes")
    recipes = db.query(Recipe).all()
    return {r.phase: json.loads(r.shares) for r in recipes}


class RecipeUpdate(BaseModel):
    phase: str
    shares: List[float]


@router.put("/recipes")
async def update_recipe(req: RecipeUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    require_write(user, "recipes")
    recipe = db.query(Recipe).filter(Recipe.phase == req.phase).first()
    if not recipe:
        raise HTTPException(status_code=404, detail=f"Faza '{req.phase}' nie znaleziona")
    recipe.shares = json.dumps(req.shares)
    db.commit()
    audit(db, user, "recipes", f"Zmieniono recepturę: {req.phase}")
    return {"ok": True}


# ══════════════════════════════════════════════════════════════════════════════
# NORMS
# ══════════════════════════════════════════════════════════════════════════════

def norm_to_dict(n):
    return {
        "phase": n.phase, "b": n.protein, "NE": n.ne,
        "Ly": n.lys, "Me": n.met, "Th": n.thr, "Tr": n.trp,
        "W": n.fiber, "Ca": n.calcium, "P": n.phosphorus
    }


@router.get("/norms")
async def get_norms(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    require_read(user, "norms")
    norms = db.query(Norm).all()
    return {n.phase: norm_to_dict(n) for n in norms}


class NormUpdate(BaseModel):
    phase: str
    b: Optional[float] = None
    NE: Optional[float] = None
    Ly: Optional[float] = None
    Me: Optional[float] = None
    Th: Optional[float] = None
    Tr: Optional[float] = None
    W: Optional[float] = None
    Ca: Optional[float] = None
    P: Optional[float] = None


@router.put("/norms")
async def update_norm(req: NormUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    require_write(user, "norms")
    norm = db.query(Norm).filter(Norm.phase == req.phase).first()
    if not norm:
        raise HTTPException(status_code=404, detail=f"Faza '{req.phase}' nie znaleziona")
    field_map = {"b": "protein", "NE": "ne", "Ly": "lys", "Me": "met",
                 "Th": "thr", "Tr": "trp", "W": "fiber", "Ca": "calcium", "P": "phosphorus"}
    for js_key, db_key in field_map.items():
        val = getattr(req, js_key, None)
        if val is not None:
            setattr(norm, db_key, val)
    db.commit()
    audit(db, user, "norms", f"Zmieniono normy: {req.phase}")
    return {"ok": True}


# ══════════════════════════════════════════════════════════════════════════════
# PRODUCTION
# ══════════════════════════════════════════════════════════════════════════════

@router.get("/production")
async def get_production(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    require_read(user, "production")
    prods = db.query(Production).all()
    return {p.phase: p.volume for p in prods}


class ProdUpdate(BaseModel):
    phase: str
    volume: float


@router.put("/production")
async def update_production(req: ProdUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    require_write(user, "production")
    prod = db.query(Production).filter(Production.phase == req.phase).first()
    if not prod:
        raise HTTPException(status_code=404, detail=f"Faza '{req.phase}' nie znaleziona")
    old = prod.volume
    prod.volume = req.volume
    db.commit()
    audit(db, user, "production", f"Zmieniono produkcję {req.phase}: {old}→{req.volume} t")
    return {"ok": True}


# ══════════════════════════════════════════════════════════════════════════════
# FULL STATE (for frontend init)
# ══════════════════════════════════════════════════════════════════════════════

@router.get("/state")
async def get_full_state(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Returns all data in one call for frontend initialization"""
    mats = db.query(Material).order_by(Material.sort_order).all()
    recipes = db.query(Recipe).all()
    norms = db.query(Norm).all()
    prods = db.query(Production).all()

    return {
        "materials": [mat_to_dict(m) for m in mats],
        "recipes": {r.phase: json.loads(r.shares) for r in recipes},
        "norms": {n.phase: norm_to_dict(n) for n in norms},
        "production": {p.phase: p.volume for p in prods},
        "user": {"id": user.id, "email": user.email, "name": user.name, "role": user.role}
    }
