from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func as sqlfunc, and_
from pydantic import BaseModel
from typing import Optional, List
from database import get_db
from models import (
    CycleRecord, FeedMonthly, FinanceRecord, YearlyStats,
    FeedSupplier, Client, ActivityLog, User, ClientAssignment
)
from auth import get_current_user, require_permission
from config import ROLE_WORKER

router = APIRouter(prefix="/api", tags=["data"])


# ═══ DASHBOARD ═══

@router.get("/dashboard")
async def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    yearly = db.query(YearlyStats).order_by(YearlyStats.year).all()
    yearly_data = [
        {"year": y.year, "cycles": y.cycles, "pigs": y.pigs,
         "profit": y.profit, "mortality": y.mortality, "fcr": y.fcr}
        for y in yearly
    ]

    # Feed supplier breakdown
    suppliers = db.query(FeedSupplier).order_by(FeedSupplier.total_pigs.desc()).limit(8).all()
    feed_data = [
        {"name": s.name, "pigs": s.total_pigs, "color": s.color}
        for s in suppliers
    ]

    # Recent cycles
    recent = db.query(CycleRecord).order_by(CycleRecord.id.desc()).limit(8).all()
    recent_data = [
        {
            "id": c.id, "cycle_number": c.cycle_number, "month": c.month,
            "client": c.client_name, "feed": c.feed,
            "startQty": c.start_qty, "soldQty": c.sold_qty,
            "profit": c.profit, "mortality": c.mortality, "type": c.cycle_type,
        }
        for c in recent
    ]

    # Summary stats
    total_clients = db.query(Client).filter(Client.is_active == True).count()
    total_cycles = sum(y.cycles for y in yearly)
    total_profit = sum(y.profit for y in yearly)
    avg_fcr = sum(y.fcr for y in yearly) / len(yearly) if yearly else 0
    avg_mort = sum(y.mortality for y in yearly) / len(yearly) if yearly else 0

    return {
        "yearlyData": yearly_data,
        "feedData": feed_data,
        "recentCycles": recent_data,
        "stats": {
            "totalCycles": total_cycles,
            "totalClients": total_clients,
            "totalProfit": total_profit,
            "avgFcr": round(avg_fcr, 2),
            "avgMortality": round(avg_mort, 2),
        },
    }


# ═══ CYCLES ═══

class CycleCreate(BaseModel):
    client_id: int
    month: str = ""
    feed: str = ""
    start_qty: int = 0
    sold_qty: int = 0
    profit: Optional[float] = None
    mortality: float = 0
    cycle_type: str = "Kabanek"
    status: str = "active"


class CycleUpdate(BaseModel):
    month: Optional[str] = None
    feed: Optional[str] = None
    start_qty: Optional[int] = None
    sold_qty: Optional[int] = None
    profit: Optional[float] = None
    mortality: Optional[float] = None
    cycle_type: Optional[str] = None
    status: Optional[str] = None


@router.get("/cycles")
async def list_cycles(
    client_id: Optional[int] = None,
    limit: int = Query(default=50, le=500),
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(CycleRecord)

    if current_user.role == ROLE_WORKER:
        assigned_ids = [
            a.client_id for a in
            db.query(ClientAssignment).filter(ClientAssignment.user_id == current_user.id).all()
        ]
        query = query.filter(CycleRecord.client_id.in_(assigned_ids)) if assigned_ids else query.filter(False)

    if client_id:
        query = query.filter(CycleRecord.client_id == client_id)

    total = query.count()
    cycles = query.order_by(CycleRecord.id.desc()).offset(offset).limit(limit).all()

    return {
        "total": total,
        "cycles": [
            {
                "id": c.id, "cycle_number": c.cycle_number, "month": c.month,
                "client_id": c.client_id, "client_name": c.client_name,
                "feed": c.feed, "start_qty": c.start_qty, "sold_qty": c.sold_qty,
                "profit": c.profit, "mortality": c.mortality,
                "cycle_type": c.cycle_type, "status": c.status,
            }
            for c in cycles
        ],
    }


@router.post("/cycles")
async def create_cycle(
    req: CycleCreate,
    current_user: User = Depends(require_permission("cycles", "create")),
    db: Session = Depends(get_db),
):
    client = db.query(Client).filter(Client.id == req.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Klient nie znaleziony")

    # Get next cycle number
    max_num = db.query(sqlfunc.max(CycleRecord.cycle_number)).scalar() or 0
    cycle = CycleRecord(
        cycle_number=max_num + 1,
        month=req.month,
        client_id=req.client_id,
        client_name=client.name,
        feed=req.feed,
        start_qty=req.start_qty,
        sold_qty=req.sold_qty,
        profit=req.profit,
        mortality=req.mortality,
        cycle_type=req.cycle_type,
        status=req.status,
    )
    db.add(cycle)
    db.add(ActivityLog(
        user_id=current_user.id, action="create", resource="cycles",
        details=f"Nowy cykl dla {client.name}: {req.start_qty} szt."
    ))
    db.commit()
    db.refresh(cycle)
    return {"id": cycle.id, "message": "Cykl dodany"}


@router.put("/cycles/{cycle_id}")
async def update_cycle(
    cycle_id: int,
    req: CycleUpdate,
    current_user: User = Depends(require_permission("cycles", "update")),
    db: Session = Depends(get_db),
):
    cycle = db.query(CycleRecord).filter(CycleRecord.id == cycle_id).first()
    if not cycle:
        raise HTTPException(status_code=404, detail="Cykl nie znaleziony")

    for field, value in req.dict(exclude_unset=True).items():
        setattr(cycle, field, value)

    db.add(ActivityLog(
        user_id=current_user.id, action="update", resource="cycles",
        resource_id=cycle_id, details=f"Zaktualizowano cykl #{cycle.cycle_number}"
    ))
    db.commit()
    return {"message": "Cykl zaktualizowany"}


@router.delete("/cycles/{cycle_id}")
async def delete_cycle(
    cycle_id: int,
    current_user: User = Depends(require_permission("cycles", "delete")),
    db: Session = Depends(get_db),
):
    cycle = db.query(CycleRecord).filter(CycleRecord.id == cycle_id).first()
    if not cycle:
        raise HTTPException(status_code=404, detail="Cykl nie znaleziony")
    db.delete(cycle)
    db.add(ActivityLog(
        user_id=current_user.id, action="delete", resource="cycles",
        resource_id=cycle_id, details=f"Usunieto cykl #{cycle.cycle_number}"
    ))
    db.commit()
    return {"message": "Cykl usuniety"}


# ═══ FEED MONTHLY ═══

@router.get("/feed")
async def get_feed_data(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(FeedMonthly)
    if start_date:
        query = query.filter(FeedMonthly.date >= start_date)
    if end_date:
        query = query.filter(FeedMonthly.date <= end_date)

    records = query.order_by(FeedMonthly.date).all()

    # Aggregate by feed
    agg = {}
    for r in records:
        if r.feed not in agg:
            agg[r.feed] = {"name": r.feed, "cycles": 0, "pigs": 0, "profit": 0,
                           "mS": 0, "fS": 0, "fC": 0}
        a = agg[r.feed]
        a["cycles"] += r.cycles
        a["pigs"] += r.pigs
        a["profit"] += r.profit
        a["mS"] += r.mortality * r.cycles
        if r.fcr > 0:
            a["fS"] += r.fcr * r.cycles
            a["fC"] += r.cycles

    feeds = []
    for f in agg.values():
        feeds.append({
            "name": f["name"],
            "cycles": f["cycles"],
            "pigs": f["pigs"],
            "profit": f["profit"],
            "mortality": round(f["mS"] / f["cycles"], 2) if f["cycles"] > 0 else 0,
            "fcr": round(f["fS"] / f["fC"], 2) if f["fC"] > 0 else 0,
        })

    feeds.sort(key=lambda x: x["pigs"], reverse=True)

    # Raw data for charts
    raw = [
        {"feed": r.feed, "ym": r.ym, "date": r.date, "cycles": r.cycles,
         "pigs": r.pigs, "profit": r.profit, "mortality": r.mortality, "fcr": r.fcr}
        for r in records
    ]

    return {"feeds": feeds, "raw": raw}


# ═══ FINANCE ═══

@router.get("/finance")
async def get_finance_data(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(FinanceRecord)
    if start_date:
        query = query.filter(FinanceRecord.date >= start_date)
    if end_date:
        query = query.filter(FinanceRecord.date <= end_date)

    records = query.order_by(FinanceRecord.date).all()

    # Worker filter: only assigned clients
    if current_user.role == ROLE_WORKER:
        assigned_ids = [
            a.client_id for a in
            db.query(ClientAssignment).filter(ClientAssignment.user_id == current_user.id).all()
        ]
        assigned_names = [
            c.name for c in
            db.query(Client).filter(Client.id.in_(assigned_ids)).all()
        ] if assigned_ids else []
        records = [r for r in records if r.client_name in assigned_names]

    # Aggregate by client
    agg = {}
    for r in records:
        cn = r.client_name
        if cn not in agg:
            agg[cn] = {
                "name": cn, "cycles": 0, "settledCycles": 0, "prelimCycles": 0,
                "inProgress": 0, "pigs": 0, "sold": 0, "profit": 0,
                "prelimProfit": 0, "mS": 0, "fS": 0, "fC": 0, "deaths": 0, "feeds": {}
            }
        a = agg[cn]
        a["cycles"] += 1
        a["pigs"] += r.pigs
        a["sold"] += r.sold
        a["mS"] += r.mortality
        a["deaths"] += r.deaths
        if r.status == 2 and r.profit is not None:
            a["profit"] += r.profit
            a["settledCycles"] += 1
        elif r.status == 1 and r.profit is not None:
            a["prelimProfit"] += r.profit
            a["prelimCycles"] += 1
        else:
            a["inProgress"] += 1
        if r.fcr > 0:
            a["fS"] += r.fcr
            a["fC"] += 1
        if r.feed:
            a["feeds"][r.feed] = 1

    clients = []
    for a in agg.values():
        tp = a["profit"] + a["prelimProfit"]
        clients.append({
            "name": a["name"],
            "cycles": a["cycles"],
            "settledCycles": a["settledCycles"],
            "prelimCycles": a["prelimCycles"],
            "inProgress": a["inProgress"],
            "pigs": a["pigs"],
            "sold": a["sold"],
            "totalProfit": tp,
            "profit": a["profit"],
            "prelimProfit": a["prelimProfit"],
            "mortality": round(a["mS"] / a["cycles"], 2) if a["cycles"] > 0 else 0,
            "fcr": round(a["fS"] / a["fC"], 2) if a["fC"] > 0 else 0,
            "deaths": a["deaths"],
            "profitPerPig": round(tp / a["sold"], 2) if a["sold"] > 0 else 0,
            "feeds": ", ".join(list(a["feeds"].keys())[:3]),
        })

    if search:
        clients = [c for c in clients if search.lower() in c["name"].lower()]

    clients.sort(key=lambda x: x["totalProfit"], reverse=True)

    # Summary
    tc = sum(c["cycles"] for c in clients)
    tp = sum(c["pigs"] for c in clients)
    tz = sum(c["totalProfit"] for c in clients)
    profit_sum = sum(c["totalProfit"] for c in clients if c["totalProfit"] > 0)
    loss_sum = sum(c["totalProfit"] for c in clients if c["totalProfit"] < 0)
    ts = sum(c["sold"] for c in clients)

    return {
        "clients": clients,
        "summary": {
            "clientCount": len(clients),
            "totalCycles": tc,
            "totalPigs": tp,
            "totalSold": ts,
            "totalProfit": tz,
            "profitSum": profit_sum,
            "lossSum": loss_sum,
            "profitable": sum(1 for c in clients if c["totalProfit"] > 0),
            "lossMaking": sum(1 for c in clients if c["totalProfit"] < 0),
            "avgProfitPerPig": round(tz / ts, 2) if ts > 0 else 0,
        },
        "raw": [
            {
                "c": r.client_name, "d": r.date, "p": r.pigs, "s": r.sold,
                "z": r.profit, "m": r.mortality, "f": r.fcr, "u": r.deaths,
                "w": r.feed, "ok": r.status,
            }
            for r in records
        ],
    }


# ═══ FEED SUPPLIERS ═══

@router.get("/suppliers")
async def list_suppliers(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    suppliers = db.query(FeedSupplier).filter(FeedSupplier.is_active == True).order_by(FeedSupplier.total_pigs.desc()).all()
    return [
        {"id": s.id, "name": s.name, "color": s.color, "total_pigs": s.total_pigs}
        for s in suppliers
    ]


# ═══ ACTIVITY LOG ═══

@router.get("/activity")
async def get_activity_log(
    limit: int = Query(default=50, le=200),
    current_user: User = Depends(require_permission("users", "read")),
    db: Session = Depends(get_db),
):
    logs = (
        db.query(ActivityLog)
        .join(User)
        .order_by(ActivityLog.created_at.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "id": l.id,
            "user": l.user.full_name,
            "action": l.action,
            "resource": l.resource,
            "details": l.details,
            "created_at": str(l.created_at) if l.created_at else None,
        }
        for l in logs
    ]


# ═══ PERMISSIONS INFO ═══

@router.get("/permissions")
async def get_my_permissions(current_user: User = Depends(get_current_user)):
    from config import PERMISSIONS
    return {
        "role": current_user.role,
        "permissions": PERMISSIONS.get(current_user.role, {}),
    }
