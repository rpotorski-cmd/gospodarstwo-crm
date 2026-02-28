from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, JSON
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="user")  # admin, user, zoo
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())


class Cycle(Base):
    """Wstawienie tuczników — główna tabela tuczarni"""
    __tablename__ = "cycles"
    id = Column(Integer, primary_key=True, index=True)
    cid = Column(String(50), nullable=False, index=True)  # chamber id (k1, k2, stara...)
    num = Column(Integer, default=1)  # cycle number for chamber
    start = Column(String(20))  # date YYYY-MM-DD
    head = Column(Integer, default=0)  # ilość sztuk
    sw = Column(Float, default=0)  # waga początkowa kg
    ew = Column(Float, default=0)  # waga końcowa kg
    dg = Column(Float, default=0)  # przyrost dzienny
    fcr = Column(Float, default=0)
    dead = Column(Integer, default=0)
    fkg = Column(Float, default=0)  # pasza kg
    fp = Column(Float, default=0)  # cena paszy zł/kg
    pc = Column(Float, default=0)  # zakup zł/szt
    vc = Column(Float, default=0)  # wet. zł/szt
    vac = Column(Float, default=0)  # szczep. zł/szt
    wc = Column(Float, default=0)  # praca zł/szt
    uc = Column(Float, default=0)  # media zł/szt
    cc = Column(Float, default=0)  # kredyt zł/szt
    kolczyk = Column(String(50), default="")  # ear tag DK
    waga_pl = Column(Float, default=0)  # waga rozładunkowa PL
    waga_dk = Column(Float, default=0)  # waga załadunkowa DK
    weigh_day = Column(Integer, default=60)
    st = Column(String(20), default="active")  # active / done
    sales = Column(JSON, default=list)  # [{d,q,k,p,ub}]
    deaths = Column(JSON, default=list)  # [{d,qty,weight,cause}]
    meds = Column(JSON, default=list)  # [{d,name,dose,qty,unit,price}]
    weighings = Column(JSON, default=list)  # [{d,day,weights:[{kg}],note}]
    todos = Column(JSON, default=list)  # [{id,name,icon,cat,desc,status,date,note}]
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Stock(Base):
    """Magazyn leków"""
    __tablename__ = "stock"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    unit = Column(String(50), default="szt")
    qty = Column(Float, default=0)
    min_qty = Column(Float, default=0)
    last_delivery = Column(String(20), default="")
    note = Column(Text, default="")


class Feed(Base):
    """Dostawy paszy"""
    __tablename__ = "feeds"
    id = Column(Integer, primary_key=True, index=True)
    d = Column(String(20))  # date
    tons = Column(Float, default=0)
    type = Column(String(50), default="Starter")
    cid = Column(String(50), default="")  # chamber id
    note = Column(Text, default="")
    zwrot = Column(Boolean, default=False)


class Paszarnia(Base):
    """Paszarnia — log + bufory stored as JSON"""
    __tablename__ = "paszarnia"
    id = Column(Integer, primary_key=True, index=True)
    data = Column(JSON, default=dict)  # {log:[], bufory:[]}


class Silosy(Base):
    """Silosy — config + log stored as JSON"""
    __tablename__ = "silosy"
    id = Column(Integer, primary_key=True, index=True)
    data = Column(JSON, default=dict)  # {silosy:[], log:[]}


class Ciagnik(Base):
    """Ciągniki i maszyny"""
    __tablename__ = "ciagniki"
    id = Column(Integer, primary_key=True, index=True)
    typ = Column(String(50), default="ciagnik")
    nazwa = Column(String(255), default="")
    marka = Column(String(255), default="")
    rok = Column(String(10), default="")
    moc = Column(String(50), default="")
    rejestr = Column(String(50), default="")
    przeglad = Column(String(20), default="")
    ubezp = Column(String(20), default="")
    uwagi = Column(Text, default="")
    olej_silnik = Column(String(100), default="")
    olej_skrzynia = Column(String(100), default="")
    olej_most_p = Column(String(100), default="")
    olej_most_t = Column(String(100), default="")
    naprawy = Column(Text, default="")


class Grunt(Base):
    """Grunty / działki"""
    __tablename__ = "grunty"
    id = Column(Integer, primary_key=True, index=True)
    nr = Column(String(100), default="")
    teryt = Column(String(100), default="")
    obreb = Column(String(255), default="")
    pow = Column(String(50), default="")
    gmina = Column(String(255), default="")
    powiat = Column(String(255), default="")
    woj = Column(String(255), default="warmińsko-mazurskie")
    nazwa = Column(String(255), default="")
    wlasciciel = Column(String(255), default="")
    uwagi = Column(Text, default="")
    kw = Column(String(100), default="")
    obciazona = Column(String(10), default="nie")
    bank_nazwa = Column(String(255), default="")
    bank_kwota = Column(String(100), default="")


class Uprawa(Base):
    """Uprawy"""
    __tablename__ = "uprawy"
    id = Column(Integer, primary_key=True, index=True)
    grunt = Column(String(255), default="")
    roslina = Column(String(255), default="")
    odmiana = Column(String(255), default="")
    pow = Column(String(50), default="")
    data_s = Column(String(20), default="")
    data_z = Column(String(20), default="")
    plon = Column(String(50), default="")
    uwagi = Column(Text, default="")


class Nawoz(Base):
    """Nawożenie"""
    __tablename__ = "nawozy"
    id = Column(Integer, primary_key=True, index=True)
    d = Column(String(20))
    grunt = Column(String(255), default="")
    nawoz = Column(String(255), default="")
    typ = Column(String(100), default="Azotowy")
    dawka = Column(String(100), default="")
    pow = Column(String(50), default="")
    uwagi = Column(Text, default="")


class Oprysk(Base):
    """Opryski"""
    __tablename__ = "opryski"
    id = Column(Integer, primary_key=True, index=True)
    d = Column(String(20))
    grunt = Column(String(255), default="")
    srodek = Column(String(255), default="")
    dawka = Column(String(100), default="")
    pow = Column(String(50), default="")
    cel = Column(String(100), default="Chwasty")
    faza = Column(String(100), default="")
    uwagi = Column(Text, default="")


class Paliwo(Base):
    """Paliwa i smary"""
    __tablename__ = "paliwa"
    id = Column(Integer, primary_key=True, index=True)
    d = Column(String(20))
    typ = Column(String(50), default="ON")
    maszyna = Column(String(255), default="")
    litry = Column(Float, default=0)
    cena = Column(Float, default=0)
    km = Column(String(50), default="")
    uwagi = Column(Text, default="")


class RDostawa(Base):
    """Dostawy — produkcja roślinna"""
    __tablename__ = "rdostawy"
    id = Column(Integer, primary_key=True, index=True)
    d = Column(String(20))
    produkt = Column(String(255), default="")
    ilosc = Column(Float, default=0)
    jm = Column(String(20), default="t")
    cena = Column(Float, default=0)
    dostawca = Column(String(255), default="")
    fv = Column(String(100), default="")
    uwagi = Column(Text, default="")


class Zakup(Base):
    """Zakupy różne"""
    __tablename__ = "zakupy"
    id = Column(Integer, primary_key=True, index=True)
    d = Column(String(20))
    produkt = Column(String(255), default="")
    cena = Column(Float, default=0)
    kto = Column(String(255), default="")
    uwagi = Column(Text, default="")


class Biogaz(Base):
    """Biogazownia"""
    __tablename__ = "biogaz"
    id = Column(Integer, primary_key=True, index=True)
    d = Column(String(20))
    kat = Column(String(50), default="inne")
    czynnosc = Column(Text, default="")
    uwagi = Column(Text, default="")
    kto = Column(String(255), default="")


class Dokument(Base):
    """Dokumenty z datami ważności + pliki PDF/skany"""
    __tablename__ = "dokumenty"
    id = Column(Integer, primary_key=True, index=True)
    kat = Column(String(50), default="inne")
    nazwa = Column(String(255), default="")
    nr = Column(String(100), default="")
    podmiot = Column(String(255), default="")
    data_od = Column(String(20), default="")
    data_do = Column(String(20), default="")
    grunt = Column(String(255), default="")
    uwagi = Column(Text, default="")
    status = Column(String(20), default="aktywny")
    # File attachment
    file_name = Column(String(500), default="")
    file_path = Column(String(500), default="")
    file_size = Column(Integer, default=0)
    file_mime = Column(String(100), default="")


class Akcyza(Base):
    """Akcyza — podmioty"""
    __tablename__ = "akcyza"
    id = Column(Integer, primary_key=True, index=True)
    nazwa = Column(String(255), nullable=False)
    typ = Column(String(100), default="")
    col = Column(String(20), default="#000")
    ha = Column(Float, default=0)
    swin = Column(Float, default=0)


class Ubojnia(Base):
    """Lista ubojni"""
    __tablename__ = "ubojnie"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)


class CustomElement(Base):
    """Admin-managed lists: medications, death causes, feed types, etc."""
    __tablename__ = "custom_elements"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(50), nullable=False, index=True)
    # categories: meds, causes, feed_types, ubojnie, bufory, silosy,
    #             biogaz_cats, doc_cats, nawoz_types, oprysk_targets, paliwo_types
    name = Column(String(255), nullable=False)
    unit = Column(String(50), default="")
    def_price = Column(Float, default=0)
    def_dose = Column(String(255), default="")
    color = Column(String(20), default="")
    icon = Column(String(10), default="")
    extra = Column(JSON, default=dict)  # any additional category-specific data
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())


class AuditLog(Base):
    """Historia zmian"""
    __tablename__ = "audit_log"
    id = Column(Integer, primary_key=True, index=True)
    ts = Column(DateTime, server_default=func.now())
    user_name = Column(String(255), default="")
    email = Column(String(255), default="")
    area = Column(String(100), default="")
    action = Column(Text, default="")
