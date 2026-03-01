from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import get_db
from models import (Ciagnik, Grunt, Uprawa, Nawoz, Oprysk, Paliwo,
                    RDostawa, Zakup, Biogaz, Dokument, Akcyza, AuditLog, User)
from auth import get_current_user
from config import can_read, can_write

router = APIRouter(prefix="/api", tags=["roslinna"])


def check_read(user, mod):
    if not can_read(user.role, mod):
        raise HTTPException(status_code=403, detail="Brak uprawnien")

def check_write(user, mod):
    if not can_write(user.role, mod):
        raise HTTPException(status_code=403, detail="Brak uprawnien")

def audit(db, user, area, action):
    db.add(AuditLog(user_name=user.name, email=user.email, area=area, action=action))
    db.commit()


# GENERIC CRUD HELPER
def make_crud(model_cls, module_name, fields, audit_area):

    async def list_all(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
        check_read(user, module_name)
        items = db.query(model_cls).order_by(model_cls.id).all()
        result = []
        for item in items:
            d = {"id": item.id}
            for f in fields:
                val = getattr(item, f["db"], None)
                d[f["js"]] = val if val is not None else f.get("default", "")
            result.append(d)
        return result

    async def create(request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
        check_write(user, module_name)
        data = await request.json()
        item = model_cls()
        for f in fields:
            if f["js"] in data:
                setattr(item, f["db"], data[f["js"]])
        db.add(item)
        db.commit()
        db.refresh(item)
        audit(db, user, audit_area, f"Dodano #{item.id}")
        return {"id": item.id}

    async def update(item_id: int, request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
        check_write(user, module_name)
        data = await request.json()
        item = db.query(model_cls).filter(model_cls.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404)
        for f in fields:
            if f["js"] in data:
                setattr(item, f["db"], data[f["js"]])
        db.commit()
        return {"ok": True}

    async def delete(item_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
        check_write(user, module_name)
        item = db.query(model_cls).filter(model_cls.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404)
        db.delete(item)
        db.commit()
        audit(db, user, audit_area, f"Usunieto #{item_id}")
        return {"ok": True}

    return list_all, create, update, delete


# CIAGNIKI / MASZYNY
_c_fields = [
    {"js":"typ","db":"typ","default":"ciagnik"}, {"js":"nazwa","db":"nazwa","default":""},
    {"js":"marka","db":"marka","default":""}, {"js":"rok","db":"rok","default":""},
    {"js":"moc","db":"moc","default":""}, {"js":"rejestr","db":"rejestr","default":""},
    {"js":"przeglad","db":"przeglad","default":""}, {"js":"ubezp","db":"ubezp","default":""},
    {"js":"uwagi","db":"uwagi","default":""}, {"js":"olejSilnik","db":"olej_silnik","default":""},
    {"js":"olejSkrzynia","db":"olej_skrzynia","default":""}, {"js":"olejMostP","db":"olej_most_p","default":""},
    {"js":"olejMostT","db":"olej_most_t","default":""}, {"js":"naprawy","db":"naprawy","default":""},
]
_cl, _cc, _cu, _cd = make_crud(Ciagnik, "ciagniki", _c_fields, "maszyny")
router.get("/ciagniki")(_cl)
router.post("/ciagniki")(_cc)
router.put("/ciagniki/{item_id}")(_cu)
router.delete("/ciagniki/{item_id}")(_cd)


# GRUNTY
_g_fields = [
    {"js":"nr","db":"nr"}, {"js":"teryt","db":"teryt"}, {"js":"obreb","db":"obreb"},
    {"js":"pow","db":"pow"}, {"js":"gmina","db":"gmina"}, {"js":"powiat","db":"powiat"},
    {"js":"woj","db":"woj","default":"warminsko-mazurskie"}, {"js":"nazwa","db":"nazwa"},
    {"js":"wlasciciel","db":"wlasciciel"}, {"js":"uwagi","db":"uwagi"},
    {"js":"kw","db":"kw"}, {"js":"obciazona","db":"obciazona","default":"nie"},
    {"js":"bankNazwa","db":"bank_nazwa"}, {"js":"bankKwota","db":"bank_kwota"},
    {"js":"umowa","db":"umowa"}, {"js":"terminUmowy","db":"termin_umowy"}, {"js":"doplaty","db":"doplaty"},
]
_gl, _gc, _gu, _gd = make_crud(Grunt, "grunty", _g_fields, "grunty")
router.get("/grunty")(_gl)
router.post("/grunty")(_gc)
router.put("/grunty/{item_id}")(_gu)
router.delete("/grunty/{item_id}")(_gd)


# UPRAWY
_u_fields = [
    {"js":"grunt","db":"grunt"}, {"js":"roslina","db":"roslina"}, {"js":"odmiana","db":"odmiana"},
    {"js":"pow","db":"pow"}, {"js":"dataS","db":"data_s"}, {"js":"dataZ","db":"data_z"},
    {"js":"plon","db":"plon"}, {"js":"uwagi","db":"uwagi"},
]
_ul, _uc2, _uu, _ud = make_crud(Uprawa, "uprawy", _u_fields, "uprawy")
router.get("/uprawy")(_ul)
router.post("/uprawy")(_uc2)
router.put("/uprawy/{item_id}")(_uu)
router.delete("/uprawy/{item_id}")(_ud)


# NAWOZY
_n_fields = [
    {"js":"d","db":"d"}, {"js":"grunt","db":"grunt"}, {"js":"nawoz","db":"nawoz"},
    {"js":"typ","db":"typ","default":"Azotowy"}, {"js":"dawka","db":"dawka"},
    {"js":"pow","db":"pow"}, {"js":"uwagi","db":"uwagi"},
]
_nl, _nc, _nu, _nd = make_crud(Nawoz, "nawozy", _n_fields, "nawozy")
router.get("/nawozy")(_nl)
router.post("/nawozy")(_nc)
router.put("/nawozy/{item_id}")(_nu)
router.delete("/nawozy/{item_id}")(_nd)


# OPRYSKI
_o_fields = [
    {"js":"d","db":"d"}, {"js":"grunt","db":"grunt"}, {"js":"srodek","db":"srodek"},
    {"js":"dawka","db":"dawka"}, {"js":"pow","db":"pow"},
    {"js":"cel","db":"cel","default":"Chwasty"}, {"js":"faza","db":"faza"},
    {"js":"uwagi","db":"uwagi"},
]
_ol, _oc, _ou, _od = make_crud(Oprysk, "opryski", _o_fields, "opryski")
router.get("/opryski")(_ol)
router.post("/opryski")(_oc)
router.put("/opryski/{item_id}")(_ou)
router.delete("/opryski/{item_id}")(_od)


# PALIWA
_p_fields = [
    {"js":"d","db":"d"}, {"js":"typ","db":"typ","default":"ON"}, {"js":"maszyna","db":"maszyna"},
    {"js":"litry","db":"litry","default":0}, {"js":"cena","db":"cena","default":0},
    {"js":"km","db":"km"}, {"js":"uwagi","db":"uwagi"},
]
_pl, _pc2, _pu, _pd = make_crud(Paliwo, "paliwa", _p_fields, "paliwa")
router.get("/paliwa")(_pl)
router.post("/paliwa")(_pc2)
router.put("/paliwa/{item_id}")(_pu)
router.delete("/paliwa/{item_id}")(_pd)


# DOSTAWY ROSLINNA
_rd_fields = [
    {"js":"d","db":"d"}, {"js":"produkt","db":"produkt"}, {"js":"ilosc","db":"ilosc","default":0},
    {"js":"jm","db":"jm","default":"t"}, {"js":"cena","db":"cena","default":0},
    {"js":"dostawca","db":"dostawca"}, {"js":"fv","db":"fv"}, {"js":"uwagi","db":"uwagi"},
]
_rdl, _rdc, _rdu, _rdd = make_crud(RDostawa, "rdostawy", _rd_fields, "dostawy")
router.get("/rdostawy")(_rdl)
router.post("/rdostawy")(_rdc)
router.put("/rdostawy/{item_id}")(_rdu)
router.delete("/rdostawy/{item_id}")(_rdd)


# ZAKUPY
_z_fields = [
    {"js":"d","db":"d"}, {"js":"produkt","db":"produkt"},
    {"js":"cena","db":"cena","default":0}, {"js":"kto","db":"kto"}, {"js":"uwagi","db":"uwagi"},
]
_zl, _zc, _zu, _zd = make_crud(Zakup, "zakupy", _z_fields, "zakupy")
router.get("/zakupy")(_zl)
router.post("/zakupy")(_zc)
router.put("/zakupy/{item_id}")(_zu)
router.delete("/zakupy/{item_id}")(_zd)


# BIOGAZOWNIA
_b_fields = [
    {"js":"d","db":"d"}, {"js":"kat","db":"kat","default":"inne"},
    {"js":"czynnosc","db":"czynnosc"}, {"js":"uwagi","db":"uwagi"}, {"js":"kto","db":"kto"},
]
_bl, _bc, _bu, _bd = make_crud(Biogaz, "biogaz", _b_fields, "biogazownia")
router.get("/biogaz")(_bl)
router.post("/biogaz")(_bc)
router.put("/biogaz/{item_id}")(_bu)
router.delete("/biogaz/{item_id}")(_bd)


# DOKUMENTY
_d_fields = [
    {"js":"kat","db":"kat","default":"inne"}, {"js":"nazwa","db":"nazwa"},
    {"js":"nr","db":"nr"}, {"js":"podmiot","db":"podmiot"},
    {"js":"dataOd","db":"data_od"}, {"js":"dataDo","db":"data_do"},
    {"js":"grunt","db":"grunt"}, {"js":"uwagi","db":"uwagi"},
    {"js":"status","db":"status","default":"aktywny"},
    {"js":"fileName","db":"file_name","default":""},
    {"js":"fileSize","db":"file_size","default":0},
    {"js":"fileMime","db":"file_mime","default":""},
]
_dl, _dc, _du2, _dd = make_crud(Dokument, "dokumenty", _d_fields, "dokumenty")
router.get("/dokumenty")(_dl)
router.post("/dokumenty")(_dc)
router.put("/dokumenty/{item_id}")(_du2)
router.delete("/dokumenty/{item_id}")(_dd)


# AKCYZA

@router.get("/akcyza")
async def list_akcyza(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_read(user, "akcyza")
    items = db.query(Akcyza).order_by(Akcyza.id).all()
    return [{"id": a.id, "nazwa": a.nazwa, "typ": a.typ, "col": a.col, "ha": a.ha, "swin": a.swin} for a in items]


@router.put("/akcyza/{aid}")
async def update_akcyza(aid: int, request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_write(user, "akcyza")
    data = await request.json()
    a = db.query(Akcyza).filter(Akcyza.id == aid).first()
    if not a:
        raise HTTPException(status_code=404)
    if "ha" in data: a.ha = float(data["ha"])
    if "swin" in data: a.swin = float(data["swin"])
    if "nazwa" in data: a.nazwa = data["nazwa"]
    if "typ" in data: a.typ = data["typ"]
    db.commit()
    return {"ok": True}
