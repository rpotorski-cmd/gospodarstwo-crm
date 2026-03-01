from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import get_db
from models import CustomElement, AuditLog, User
from auth import get_current_user, require_role
from config import ROLE_ADMIN

router = APIRouter(prefix="/api/admin", tags=["admin"])


def audit(db, user, area, action):
    db.add(AuditLog(user_name=user.name, email=user.email, area=area, action=action))
    db.commit()


VALID_CATEGORIES = [
    "meds", "causes", "feed_types", "ubojnie", "bufory",
    "biogaz_cats", "doc_cats", "nawoz_types", "oprysk_targets",
    "paliwo_types", "todos_def"
]


@router.get("/elements")
async def list_all_elements(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    items = db.query(CustomElement).order_by(
        CustomElement.category, CustomElement.sort_order, CustomElement.id
    ).all()
    result = {}
    for el in items:
        cat = el.category
        if cat not in result:
            result[cat] = []
        result[cat].append(_el_to_dict(el))
    return result


@router.get("/elements/{category}")
async def list_elements_by_category(
    category: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if category not in VALID_CATEGORIES:
        raise HTTPException(status_code=400, detail=f"Nieprawidlowa kategoria: {category}")
    items = db.query(CustomElement).filter(
        CustomElement.category == category
    ).order_by(CustomElement.sort_order, CustomElement.id).all()
    return [_el_to_dict(el) for el in items]


@router.post("/elements")
async def create_element(
    request: Request,
    user: User = Depends(require_role(ROLE_ADMIN)),
    db: Session = Depends(get_db)
):
    data = await request.json()
    cat = data.get("category", "")
    if cat not in VALID_CATEGORIES:
        raise HTTPException(status_code=400, detail=f"Nieprawidlowa kategoria: {cat}")
    name = data.get("name", "").strip()
    if not name:
        raise HTTPException(status_code=400, detail="Nazwa wymagana")

    existing = db.query(CustomElement).filter(
        CustomElement.category == cat,
        CustomElement.name == name
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Element '{name}' juz istnieje w tej kategorii")

    max_order = db.query(CustomElement).filter(
        CustomElement.category == cat
    ).count()

    el = CustomElement(
        category=cat,
        name=name,
        unit=data.get("unit", ""),
        def_price=float(data.get("defPrice", 0)),
        def_dose=data.get("defDose", ""),
        color=data.get("color", ""),
        icon=data.get("icon", ""),
        extra=data.get("extra", {}),
        sort_order=max_order,
        is_active=True,
    )
    db.add(el)
    db.commit()
    db.refresh(el)
    audit(db, user, "admin", f"Dodano element [{cat}]: {name}")
    return _el_to_dict(el)


@router.put("/elements/{eid}")
async def update_element(
    eid: int,
    request: Request,
    user: User = Depends(require_role(ROLE_ADMIN)),
    db: Session = Depends(get_db)
):
    data = await request.json()
    el = db.query(CustomElement).filter(CustomElement.id == eid).first()
    if not el:
        raise HTTPException(status_code=404, detail="Nie znaleziono")

    if "name" in data: el.name = data["name"]
    if "unit" in data: el.unit = data["unit"]
    if "defPrice" in data: el.def_price = float(data["defPrice"])
    if "defDose" in data: el.def_dose = data["defDose"]
    if "color" in data: el.color = data["color"]
    if "icon" in data: el.icon = data["icon"]
    if "extra" in data: el.extra = data["extra"]
    if "sortOrder" in data: el.sort_order = int(data["sortOrder"])
    if "isActive" in data: el.is_active = bool(data["isActive"])

    db.commit()
    audit(db, user, "admin", f"Zaktualizowano element [{el.category}]: {el.name}")
    return _el_to_dict(el)


@router.delete("/elements/{eid}")
async def delete_element(
    eid: int,
    user: User = Depends(require_role(ROLE_ADMIN)),
    db: Session = Depends(get_db)
):
    el = db.query(CustomElement).filter(CustomElement.id == eid).first()
    if not el:
        raise HTTPException(status_code=404, detail="Nie znaleziono")
    name = el.name
    cat = el.category
    el.is_active = False
    db.commit()
    audit(db, user, "admin", f"Dezaktywowano element [{cat}]: {name}")
    return {"ok": True}


@router.delete("/elements/{eid}/permanent")
async def hard_delete_element(
    eid: int,
    user: User = Depends(require_role(ROLE_ADMIN)),
    db: Session = Depends(get_db)
):
    el = db.query(CustomElement).filter(CustomElement.id == eid).first()
    if not el:
        raise HTTPException(status_code=404, detail="Nie znaleziono")
    name = el.name
    cat = el.category
    db.delete(el)
    db.commit()
    audit(db, user, "admin", f"Usunieto trwale element [{cat}]: {name}")
    return {"ok": True}


@router.put("/elements/reorder/{category}")
async def reorder_elements(
    category: str,
    request: Request,
    user: User = Depends(require_role(ROLE_ADMIN)),
    db: Session = Depends(get_db)
):
    data = await request.json()
    order = data.get("order", [])
    for idx, eid in enumerate(order):
        el = db.query(CustomElement).filter(
            CustomElement.id == eid, CustomElement.category == category
        ).first()
        if el:
            el.sort_order = idx
    db.commit()
    return {"ok": True}


def _el_to_dict(el):
    return {
        "id": el.id,
        "category": el.category,
        "name": el.name,
        "unit": el.unit,
        "defPrice": el.def_price,
        "defDose": el.def_dose,
        "color": el.color,
        "icon": el.icon,
        "extra": el.extra or {},
        "sortOrder": el.sort_order,
        "isActive": el.is_active,
    }
