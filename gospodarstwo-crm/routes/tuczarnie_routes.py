from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List, Any
from database import get_db
from models import Cycle, Stock, Feed, Paszarnia, Silosy, Ubojnia, AuditLog, User
from auth import get_current_user
from config import can_read, can_write

router = APIRouter(prefix="/api", tags=["tuczarnie"])


def check_read(user, module):
    if not can_read(user.role, module):
        raise HTTPException(status_code=403, detail="Brak uprawnien do odczytu")


def check_write(user, module):
    if not can_write(user.role, module):
        raise HTTPException(status_code=403, detail="Brak uprawnien do zapisu")


def audit(db, user, area, action):
    db.add(AuditLog(user_name=user.name, email=user.email, area=area, action=action))
    db.commit()


# CYCLES (wstawienia)

class CycleCreate(BaseModel):
    cid: str
    num: int = 1
    start: str = ""
    head: int = 0
    sw: float = 0
    fp: float = 0
    pc: float = 0
    vc: float = 0
    vac: float = 0
    wc: float = 0
    uc: float = 0
    cc: float = 0
    kolczyk: str = ""
    wagaPL: float = 0
    wagaDK: float = 0
    todos: list = []


class CycleUpdate(BaseModel):
    head: Optional[int] = None
    sw: Optional[float] = None
    ew: Optional[float] = None
    dg: Optional[float] = None
    fcr: Optional[float] = None
    dead: Optional[int] = None
    fkg: Optional[float] = None
    fp: Optional[float] = None
    pc: Optional[float] = None
    vc: Optional[float] = None
    vac: Optional[float] = None
    wc: Optional[float] = None
    uc: Optional[float] = None
    cc: Optional[float] = None
    kolczyk: Optional[str] = None
    waga_pl: Optional[float] = None
    waga_dk: Optional[float] = None
    weigh_day: Optional[int] = None
    st: Optional[str] = None
    sales: Optional[list] = None
    deaths: Optional[list] = None
    meds: Optional[list] = None
    weighings: Optional[list] = None
    todos: Optional[list] = None


def cycle_to_dict(c):
    return {
        "id": c.id, "cid": c.cid, "num": c.num, "start": c.start,
        "head": c.head, "sw": c.sw, "ew": c.ew, "dg": c.dg, "fcr": c.fcr,
        "dead": c.dead, "fkg": c.fkg, "fp": c.fp, "pc": c.pc, "vc": c.vc,
        "vac": c.vac, "wc": c.wc, "uc": c.uc, "cc": c.cc,
        "kolczyk": c.kolczyk, "wagaPL": c.waga_pl, "wagaDK": c.waga_dk,
        "weighDay": c.weigh_day, "st": c.st,
        "sales": c.sales or [], "deaths": c.deaths or [],
        "meds": c.meds or [], "weighings": c.weighings or [],
        "todos": c.todos or [],
    }


@router.get("/cycles")
async def list_cycles(cid: Optional[str] = None, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_read(user, "cycles")
    q = db.query(Cycle)
    if cid:
        q = q.filter(Cycle.cid == cid)
    cycles = q.order_by(Cycle.id).all()
    return [cycle_to_dict(c) for c in cycles]


@router.post("/cycles")
async def create_cycle(req: CycleCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_write(user, "cycles")
    c = Cycle(
        cid=req.cid, num=req.num, start=req.start, head=req.head,
        sw=req.sw, fp=req.fp, pc=req.pc, vc=req.vc, vac=req.vac,
        wc=req.wc, uc=req.uc, cc=req.cc, kolczyk=req.kolczyk,
        waga_pl=req.wagaPL, waga_dk=req.wagaDK,
        weigh_day=60, st="active",
        sales=[], deaths=[], meds=[], weighings=[],
        todos=req.todos or [],
    )
    db.add(c)
    db.commit()
    db.refresh(c)
    audit(db, user, "tuczarnie", f"Nowe wstawienie: komora {req.cid} #{req.num} ({req.head} szt)")
    return cycle_to_dict(c)


@router.put("/cycles/{cid}")
async def update_cycle(cid: int, req: CycleUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_write(user, "cycles")
    c = db.query(Cycle).filter(Cycle.id == cid).first()
    if not c:
        raise HTTPException(status_code=404, detail="Nie znaleziono")
    for field, value in req.dict(exclude_unset=True).items():
        if field == "waga_pl":
            c.waga_pl = value
        elif field == "waga_dk":
            c.waga_dk = value
        elif field == "weigh_day":
            c.weigh_day = value
        elif hasattr(c, field):
            setattr(c, field, value)
    db.commit()
    return cycle_to_dict(c)


@router.delete("/cycles/{cid}")
async def delete_cycle(cid: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Tylko administrator może usuwać dane")
    check_write(user, "cycles")
    c = db.query(Cycle).filter(Cycle.id == cid).first()
    if not c:
        raise HTTPException(status_code=404, detail="Nie znaleziono")
    db.delete(c)
    db.commit()
    audit(db, user, "tuczarnie", f"Usunieto wstawienie #{cid}")
    return {"ok": True}


@router.delete("/cycles/chamber/{chamber_id}")
async def clear_chamber(chamber_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Tylko administrator może usuwać dane")
    check_write(user, "cycles")
    db.query(Cycle).filter(Cycle.cid == chamber_id).delete()
    db.commit()
    audit(db, user, "tuczarnie", f"Wyczyszczono komore {chamber_id}")
    return {"ok": True}


# STOCK (magazyn lekow)

@router.get("/stock")
async def list_stock(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_read(user, "stock")
    items = db.query(Stock).order_by(Stock.id).all()
    return [{"id": s.id, "name": s.name, "unit": s.unit, "qty": s.qty, "minQty": s.min_qty, "lastDelivery": s.last_delivery, "note": s.note} for s in items]


@router.put("/stock/{sid}")
async def update_stock(sid: int, request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_write(user, "stock")
    data = await request.json()
    s = db.query(Stock).filter(Stock.id == sid).first()
    if not s:
        raise HTTPException(status_code=404)
    if "qty" in data: s.qty = data["qty"]
    if "minQty" in data: s.min_qty = data["minQty"]
    if "lastDelivery" in data: s.last_delivery = data["lastDelivery"]
    if "note" in data: s.note = data["note"]
    if "name" in data: s.name = data["name"]
    if "unit" in data: s.unit = data["unit"]
    db.commit()
    return {"ok": True}


@router.post("/stock")
async def add_stock(request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_write(user, "stock")
    data = await request.json()
    s = Stock(name=data.get("name", "Nowy lek"), unit=data.get("unit", "szt"))
    db.add(s)
    db.commit()
    db.refresh(s)
    return {"id": s.id}


# FEEDS (dostawy paszy)

@router.get("/feeds")
async def list_feeds(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_read(user, "feeds")
    items = db.query(Feed).order_by(Feed.id.desc()).all()
    return [{"id": f.id, "d": f.d, "tons": f.tons, "type": f.type, "cid": f.cid, "note": f.note, "zwrot": f.zwrot} for f in items]


@router.post("/feeds")
async def add_feed(request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_write(user, "feeds")
    data = await request.json()
    f = Feed(d=data.get("d",""), tons=data.get("tons",0), type=data.get("type","Starter"), cid=data.get("cid",""), note=data.get("note",""), zwrot=data.get("zwrot",False))
    db.add(f)
    db.commit()
    db.refresh(f)
    return {"id": f.id}


@router.put("/feeds/{fid}")
async def update_feed(fid: int, request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_write(user, "feeds")
    data = await request.json()
    f = db.query(Feed).filter(Feed.id == fid).first()
    if not f:
        raise HTTPException(status_code=404)
    for k in ["d","tons","type","cid","note","zwrot"]:
        if k in data:
            setattr(f, k, data[k])
    db.commit()
    return {"ok": True}


@router.delete("/feeds/{fid}")
async def delete_feed(fid: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Tylko administrator może usuwać dane")
    check_write(user, "feeds")
    db.query(Feed).filter(Feed.id == fid).delete()
    db.commit()
    return {"ok": True}


# PASZARNIA (singleton JSON)

@router.get("/paszarnia")
async def get_paszarnia(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_read(user, "paszarnia")
    p = db.query(Paszarnia).first()
    return p.data if p else {"log": [], "bufory": []}


@router.put("/paszarnia")
async def update_paszarnia(request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_write(user, "paszarnia")
    data = await request.json()
    p = db.query(Paszarnia).first()
    if not p:
        p = Paszarnia(data=data)
        db.add(p)
    else:
        p.data = data
    db.commit()
    return {"ok": True}


# SILOSY (singleton JSON)

@router.get("/silosy")
async def get_silosy(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_read(user, "silosy")
    s = db.query(Silosy).first()
    return s.data if s else {"silosy": [], "log": []}


@router.put("/silosy")
async def update_silosy(request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_write(user, "silosy")
    data = await request.json()
    s = db.query(Silosy).first()
    if not s:
        s = Silosy(data=data)
        db.add(s)
    else:
        s.data = data
    db.commit()
    return {"ok": True}


# UBOJNIE

@router.get("/ubojnie")
async def list_ubojnie(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_read(user, "ubojnie")
    return [{"id": u.id, "name": u.name} for u in db.query(Ubojnia).all()]


@router.post("/ubojnie")
async def add_ubojnia(request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_write(user, "ubojnie")
    data = await request.json()
    name = data.get("name", "")
    if not name:
        raise HTTPException(status_code=400, detail="Nazwa wymagana")
    u = Ubojnia(name=name)
    db.add(u)
    db.commit()
    db.refresh(u)
    return {"id": u.id, "name": u.name}
