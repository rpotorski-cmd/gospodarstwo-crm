from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user, require_role
from models import (
    User, Dezynfekcja, SrodekBiobojczy, Mata, PrzegladBudynku,
    KontrolaInsekty, TransportBio, DeratyzacjaBiogaz, Deratyzacja
)

router = APIRouter(prefix="/api/bio", tags=["Bioasekuracja"])

def _list(model, db):
    return db.query(model).order_by(model.id.desc()).all()

def _get(model, item_id, db):
    obj = db.query(model).filter(model.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Nie znaleziono")
    return obj

def _create(model, data, db):
    obj = model(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def _update(model, item_id, data, db):
    obj = db.query(model).filter(model.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Nie znaleziono")
    for k, v in data.items():
        if hasattr(obj, k):
            setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

def _delete(model, item_id, db):
    obj = db.query(model).filter(model.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Nie znaleziono")
    db.delete(obj)
    db.commit()
    return {"ok": True}

# 1. DEZYNFEKCJA
@router.get("/dezynfekcja")
def list_dezynfekcja(db: Session = Depends(get_db), u: User = Depends(get_current_user)):
    return _list(Dezynfekcja, db)
@router.get("/dezynfekcja/{id}")
def get_dezynfekcja(id: int, db: Session = Depends(get_db), u: User = Depends(get_current_user)):
    return _get(Dezynfekcja, id, db)
@router.post("/dezynfekcja")
def create_dezynfekcja(data: dict, db: Session = Depends(get_db), u: User = Depends(require_role("admin","user"))):
    return _create(Dezynfekcja, data, db)
@router.put("/dezynfekcja/{id}")
def update_dezynfekcja(id: int, data: dict, db: Session = Depends(get_db), u: User = Depends(require_role("admin","user"))):
    return _update(Dezynfekcja, id, data, db)
@router.delete("/dezynfekcja/{id}")
def delete_dezynfekcja(id: int, db: Session = Depends(get_db), u: User = Depends(require_role("admin"))):
    return _delete(Dezynfekcja, id, db)

# 2. SRODKI BIOBOJCZE
@router.get("/biobojcze")
def list_biobojcze(db: Session = Depends(get_db), u: User = Depends(get_current_user)):
    return _list(SrodekBiobojczy, db)
@router.get("/biobojcze/{id}")
def get_biobojcze(id: int, db: Session = Depends(get_db), u: User = Depends(get_current_user)):
    return _get(SrodekBiobojczy, id, db)
@router.post("/biobojcze")
def create_biobojcze(data: dict, db: Session = Depends(get_db), u: User = Depends(require_role("admin","user"))):
    return _create(SrodekBiobojczy, data, db)
@router.put("/biobojcze/{id}")
def update_biobojcze(id: int, data: dict, db: Session = Depends(get_db), u: User = Depends(require_role("admin","user"))):
    return _update(SrodekBiobojczy, id, data, db)
@router.delete("/biobojcze/{id}")
def delete_biobojcze(id: int, db: Session = Depends(get_db), u: User = Depends(require_role("admin"))):
    return _delete(SrodekBiobojczy, id, db)

# 3. MATY
@router.get("/maty")
def list_maty(db: Session = Depends(get_db), u: User = Depends(get_current_user)):
    return _list(Mata, db)
@router.get("/maty/{id}")
def get_mata(id: int, db: Session = Depends(get_db), u: User = Depends(get_current_user)):
    return _get(Mata, id, db)
@router.post("/maty")
def create_mata(data: dict, db: Session = Depends(get_db), u: User = Depends(require_role("admin","user"))):
    return _create(Mata, data, db)
@router.put("/maty/{id}")
def update_mata(id: int, data: dict, db: Session = Depends(get_db), u: User = Depends(require_role("admin","user"))):
    return _update(Mata, id, data, db)
@router.delete("/maty/{id}")
def delete_mata(id: int, db: Session = Depends(get_db), u: User = Depends(require_role("admin"))):
    return _delete(Mata, id, db)

# 4. PRZEGLADY BUDYNKOW
@router.get("/przeglady")
def list_przeglady(db: Session = Depends(get_db), u: User = Depends(get_current_user)):
    return _list(PrzegladBudynku, db)
@router.get("/przeglady/{id}")
def get_przeglad(id: int, db: Session = Depends(get_db), u: User = Depends(get_current_user)):
    return _get(PrzegladBudynku, id, db)
@router.post("/przeglady")
def create_przeglad(data: dict, db: Session = Depends(get_db), u: User = Depends(require_role("admin","user"))):
    return _create(PrzegladBudynku, data, db)
@router.put("/przeglady/{id}")
def update_przeglad(id: int, data: dict, db: Session = Depends(get_db), u: User = Depends(require_role("admin","user"))):
    return _update(PrzegladBudynku, id, data, db)
@router.delete("/przeglady/{id}")
def delete_przeglad(id: int, db: Session = Depends(get_db), u: User = Depends(require_role("admin"))):
    return _delete(PrzegladBudynku, id, db)

# 5. INSEKTY
@router.get("/insekty")
def list_insekty(db: Session = Depends(get_db), u: User = Depends(get_current_user)):
    return _list(KontrolaInsekty, db)
@router.get("/insekty/{id}")
def get_insekty(id: int, db: Session = Depends(get_db), u: User = Depends(get_current_user)):
    return _get(KontrolaInsekty, id, db)
@router.post("/insekty")
def create_insekty(data: dict, db: Session = Depends(get_db), u: User = Depends(require_role("admin","user"))):
    return _create(KontrolaInsekty, data, db)
@router.put("/insekty/{id}")
def update_insekty(id: int, data: dict, db: Session = Depends(get_db), u: User = Depends(require_role("admin","user"))):
    return _update(KontrolaInsekty, id, data, db)
@router.delete("/insekty/{id}")
def delete_insekty(id: int, db: Session = Depends(get_db), u: User = Depends(require_role("admin"))):
    return _delete(KontrolaInsekty, id, db)

# 6. TRANSPORT
@router.get("/transport")
def list_transport(db: Session = Depends(get_db), u: User = Depends(get_current_user)):
    return _list(TransportBio, db)
@router.get("/transport/{id}")
def get_transport(id: int, db: Session = Depends(get_db), u: User = Depends(get_current_user)):
    return _get(TransportBio, id, db)
@router.post("/transport")
def create_transport(data: dict, db: Session = Depends(get_db), u: User = Depends(require_role("admin","user"))):
    return _create(TransportBio, data, db)
@router.put("/transport/{id}")
def update_transport(id: int, data: dict, db: Session = Depends(get_db), u: User = Depends(require_role("admin","user"))):
    return _update(TransportBio, id, data, db)
@router.delete("/transport/{id}")
def delete_transport(id: int, db: Session = Depends(get_db), u: User = Depends(require_role("admin"))):
    return _delete(TransportBio, id, db)

# 7. DERATYZACJA BIOGAZOWNIA
@router.get("/deratyzacja-biogaz")
def list_derat_biogaz(db: Session = Depends(get_db), u: User = Depends(get_current_user)):
    return _list(DeratyzacjaBiogaz, db)
@router.get("/deratyzacja-biogaz/{id}")
def get_derat_biogaz(id: int, db: Session = Depends(get_db), u: User = Depends(get_current_user)):
    return _get(DeratyzacjaBiogaz, id, db)
@router.post("/deratyzacja-biogaz")
def create_derat_biogaz(data: dict, db: Session = Depends(get_db), u: User = Depends(require_role("admin","user"))):
    return _create(DeratyzacjaBiogaz, data, db)
@router.put("/deratyzacja-biogaz/{id}")
def update_derat_biogaz(id: int, data: dict, db: Session = Depends(get_db), u: User = Depends(require_role("admin","user"))):
    return _update(DeratyzacjaBiogaz, id, data, db)
@router.delete("/deratyzacja-biogaz/{id}")
def delete_derat_biogaz(id: int, db: Session = Depends(get_db), u: User = Depends(require_role("admin"))):
    return _delete(DeratyzacjaBiogaz, id, db)

# 8. DERATYZACJA OGOLNA
@router.get("/deratyzacja")
def list_deratyzacja(db: Session = Depends(get_db), u: User = Depends(get_current_user)):
    return _list(Deratyzacja, db)
@router.get("/deratyzacja/{id}")
def get_deratyzacja(id: int, db: Session = Depends(get_db), u: User = Depends(get_current_user)):
    return _get(Deratyzacja, id, db)
@router.post("/deratyzacja")
def create_deratyzacja(data: dict, db: Session = Depends(get_db), u: User = Depends(require_role("admin","user"))):
    return _create(Deratyzacja, data, db)
@router.put("/deratyzacja/{id}")
def update_deratyzacja(id: int, data: dict, db: Session = Depends(get_db), u: User = Depends(require_role("admin","user"))):
    return _update(Deratyzacja, id, data, db)
@router.delete("/deratyzacja/{id}")
def delete_deratyzacja(id: int, db: Session = Depends(get_db), u: User = Depends(require_role("admin"))):
    return _delete(Deratyzacja, id, db)
