from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, JSON, LargeBinary
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="user")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())


class Cycle(Base):
    __tablename__ = "cycles"
    id = Column(Integer, primary_key=True, index=True)
    cid = Column(String(50), nullable=False, index=True)
    num = Column(Integer, default=1)
    start = Column(String(20))
    head = Column(Integer, default=0)
    sw = Column(Float, default=0)
    ew = Column(Float, default=0)
    dg = Column(Float, default=0)
    fcr = Column(Float, default=0)
    dead = Column(Integer, default=0)
    fkg = Column(Float, default=0)
    fp = Column(Float, default=0)
    pc = Column(Float, default=0)
    vc = Column(Float, default=0)
    vac = Column(Float, default=0)
    wc = Column(Float, default=0)
    uc = Column(Float, default=0)
    cc = Column(Float, default=0)
    kolczyk = Column(String(50), default="")
    waga_pl = Column(Float, default=0)
    waga_dk = Column(Float, default=0)
    weigh_day = Column(Integer, default=60)
    st = Column(String(20), default="active")
    sales = Column(JSON, default=list)
    deaths = Column(JSON, default=list)
    meds = Column(JSON, default=list)
    weighings = Column(JSON, default=list)
    todos = Column(JSON, default=list)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Stock(Base):
    __tablename__ = "stock"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    unit = Column(String(50), default="szt")
    qty = Column(Float, default=0)
    min_qty = Column(Float, default=0)
    last_delivery = Column(String(20), default="")
    note = Column(Text, default="")


class Feed(Base):
    __tablename__ = "feeds"
    id = Column(Integer, primary_key=True, index=True)
    d = Column(String(20))
    tons = Column(Float, default=0)
    type = Column(String(50), default="Starter")
    cid = Column(String(50), default="")
    note = Column(Text, default="")
    zwrot = Column(Boolean, default=False)


class Paszarnia(Base):
    __tablename__ = "paszarnia"
    id = Column(Integer, primary_key=True, index=True)
    data = Column(JSON, default=dict)


class Silosy(Base):
    __tablename__ = "silosy"
    id = Column(Integer, primary_key=True, index=True)
    data = Column(JSON, default=dict)


class Ciagnik(Base):
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
    __tablename__ = "grunty"
    id = Column(Integer, primary_key=True, index=True)
    nr = Column(String(100), default="")
    teryt = Column(String(100), default="")
    obreb = Column(String(255), default="")
    pow = Column(String(50), default="")
    gmina = Column(String(255), default="")
    powiat = Column(String(255), default="")
    woj = Column(String(255), default="warminsko-mazurskie")
    nazwa = Column(String(255), default="")
    wlasciciel = Column(String(255), default="")
    uwagi = Column(Text, default="")
    kw = Column(String(100), default="")
    obciazona = Column(String(10), default="nie")
    bank_nazwa = Column(String(255), default="")
    bank_kwota = Column(String(100), default="")
    umowa = Column(String(255), default="")
    termin_umowy = Column(String(20), default="")
    doplaty = Column(String(100), default="")


class Uprawa(Base):
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
    __tablename__ = "zakupy"
    id = Column(Integer, primary_key=True, index=True)
    d = Column(String(20))
    produkt = Column(String(255), default="")
    cena = Column(Float, default=0)
    kto = Column(String(255), default="")
    uwagi = Column(Text, default="")


class Biogaz(Base):
    __tablename__ = "biogaz"
    id = Column(Integer, primary_key=True, index=True)
    d = Column(String(20))
    kat = Column(String(50), default="inne")
    czynnosc = Column(Text, default="")
    uwagi = Column(Text, default="")
    kto = Column(String(255), default="")


class Dokument(Base):
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
    file_name = Column(String(500), default="")
    file_path = Column(String(500), default="")
    file_size = Column(Integer, default=0)
    file_mime = Column(String(100), default="")
    file_data = Column(LargeBinary, default=None)


class Akcyza(Base):
    __tablename__ = "akcyza"
    id = Column(Integer, primary_key=True, index=True)
    nazwa = Column(String(255), nullable=False)
    typ = Column(String(100), default="")
    col = Column(String(20), default="#000")
    ha = Column(Float, default=0)
    swin = Column(Float, default=0)


class Ubojnia(Base):
    __tablename__ = "ubojnie"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)


class CustomElement(Base):
    __tablename__ = "custom_elements"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(50), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    unit = Column(String(50), default="")
    def_price = Column(Float, default=0)
    def_dose = Column(String(255), default="")
    color = Column(String(20), default="")
    icon = Column(String(10), default="")
    extra = Column(JSON, default=dict)
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())


class AuditLog(Base):
    __tablename__ = "audit_log"
    id = Column(Integer, primary_key=True, index=True)
    ts = Column(DateTime, server_default=func.now())
    user_name = Column(String(255), default="")
    email = Column(String(255), default="")
    area = Column(String(100), default="")
    action = Column(Text, default="")


# ══════════════════════════════════════════════════════════════════
#  BIOASEKURACJA — 8 rejestrow
# ══════════════════════════════════════════════════════════════════

class Dezynfekcja(Base):
    __tablename__ = "bio_dezynfekcja"
    id = Column(Integer, primary_key=True, index=True)
    d = Column(String(20), default="")
    budynek = Column(String(255), default="")
    srodek = Column(String(255), default="")
    stezenie = Column(String(100), default="")
    metoda = Column(String(100), default="oprysk")
    powierzchnia = Column(String(100), default="")
    czas_karencji = Column(String(100), default="")
    wykonawca = Column(String(255), default="")
    uwagi = Column(Text, default="")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class SrodekBiobojczy(Base):
    __tablename__ = "bio_srodki_biobojcze"
    id = Column(Integer, primary_key=True, index=True)
    d = Column(String(20), default="")
    nazwa_srodka = Column(String(255), default="")
    nr_pozwolenia = Column(String(100), default="")
    substancja_czynna = Column(String(255), default="")
    rodzaj = Column(String(100), default="")
    dawka = Column(String(100), default="")
    miejsce = Column(String(255), default="")
    powierzchnia = Column(String(100), default="")
    wykonawca = Column(String(255), default="")
    uwagi = Column(Text, default="")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Mata(Base):
    __tablename__ = "bio_maty"
    id = Column(Integer, primary_key=True, index=True)
    d = Column(String(20), default="")
    lokalizacja = Column(String(255), default="")
    typ_maty = Column(String(100), default="")
    srodek = Column(String(255), default="")
    stezenie = Column(String(100), default="")
    akcja = Column(String(100), default="wymiana")
    stan = Column(String(100), default="ok")
    wykonawca = Column(String(255), default="")
    uwagi = Column(Text, default="")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class PrzegladBudynku(Base):
    __tablename__ = "bio_przeglad_budynkow"
    id = Column(Integer, primary_key=True, index=True)
    d = Column(String(20), default="")
    budynek = Column(String(255), default="")
    siatki_okna = Column(String(50), default="ok")
    siatki_wloty = Column(String(50), default="ok")
    drzwi = Column(String(50), default="ok")
    sciany = Column(String(50), default="ok")
    dach = Column(String(50), default="ok")
    ogrodzenie = Column(String(50), default="ok")
    rynny_odplyw = Column(String(50), default="ok")
    inne_uwagi = Column(Text, default="")
    wykonawca = Column(String(255), default="")
    nastepny_przeglad = Column(String(20), default="")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class KontrolaInsekty(Base):
    __tablename__ = "bio_kontrola_insekty"
    id = Column(Integer, primary_key=True, index=True)
    d = Column(String(20), default="")
    nr_stacji = Column(String(100), default="")
    lokalizacja = Column(String(255), default="")
    typ_stacji = Column(String(100), default="")
    stan = Column(String(100), default="ok")
    ilosc_owadow = Column(String(100), default="")
    akcja = Column(String(100), default="kontrola")
    srodek = Column(String(255), default="")
    wykonawca = Column(String(255), default="")
    uwagi = Column(Text, default="")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class TransportBio(Base):
    __tablename__ = "bio_transport"
    id = Column(Integer, primary_key=True, index=True)
    d = Column(String(20), default="")
    nr_rej = Column(String(100), default="")
    kierowca = Column(String(255), default="")
    firma = Column(String(255), default="")
    cel_wizyty = Column(String(255), default="")
    dezynfekcja_przed = Column(Boolean, default=False)
    dezynfekcja_po = Column(Boolean, default=False)
    srodek_dezyn = Column(String(255), default="")
    godz_wjazdu = Column(String(10), default="")
    godz_wyjazdu = Column(String(10), default="")
    uwagi = Column(Text, default="")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class DeratyzacjaBiogaz(Base):
    __tablename__ = "bio_deratyzacja_biogaz"
    id = Column(Integer, primary_key=True, index=True)
    d = Column(String(20), default="")
    nr_stacji = Column(String(100), default="")
    lokalizacja = Column(String(255), default="biogazownia")
    preparat = Column(String(255), default="")
    dawka = Column(String(100), default="")
    zuzycie = Column(String(100), default="")
    aktywnosc = Column(String(100), default="brak")
    stan_stacji = Column(String(100), default="ok")
    wykonawca = Column(String(255), default="")
    uwagi = Column(Text, default="")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Deratyzacja(Base):
    __tablename__ = "bio_deratyzacja"
    id = Column(Integer, primary_key=True, index=True)
    d = Column(String(20), default="")
    nr_stacji = Column(String(100), default="")
    lokalizacja = Column(String(255), default="")
    budynek = Column(String(255), default="")
    preparat = Column(String(255), default="")
    dawka = Column(String(100), default="")
    zuzycie = Column(String(100), default="")
    aktywnosc = Column(String(100), default="brak")
    stan_stacji = Column(String(100), default="ok")
    wykonawca = Column(String(255), default="")
    uwagi = Column(Text, default="")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
