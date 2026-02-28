"""Seed initial data from HTML constants into database"""
from database import SessionLocal
from models import User, Stock, Ubojnia, Akcyza, Paszarnia, Silosy, CustomElement
from auth import hash_password


USERS = [
    {"email": "r.potorski@kabanek.pl", "pass": "Treder02@", "name": "Robert Potorski", "role": "admin"},
    {"email": "i.staszynska@kabanek.pl", "pass": "KabanekOsowka", "name": "Iwona Staszyńska", "role": "user"},
    {"email": "k.potorska@kabanek.pl", "pass": "Nowehaslo123", "name": "Kinga Potorska", "role": "user"},
    {"email": "zootechnik", "pass": "osowka", "name": "Zootechnik", "role": "zoo"},
]

MEDS = [
    {"name": "Denaturat", "unit": "l", "defPrice": 8.50, "defDose": "500ml/1000l wody"},
    {"name": "Wrzodex Premium", "unit": "kg", "defPrice": 18.00, "defDose": "2kg/t paszy"},
    {"name": "Zakwaszacz pH Opti", "unit": "kg", "defPrice": 4.50, "defDose": "3kg/t paszy"},
    {"name": "Zakwaszacz Green Dry", "unit": "kg", "defPrice": 5.20, "defDose": "2-4kg/t paszy"},
    {"name": "Probiotyk", "unit": "kg", "defPrice": 45.00, "defDose": "0.5kg/t paszy"},
    {"name": "Panacur", "unit": "g", "defPrice": 0.85, "defDose": "5mg/kg m.c."},
    {"name": "Amoksycylina", "unit": "g", "defPrice": 0.42, "defDose": "20mg/kg m.c./dzień"},
    {"name": "Tiamulin", "unit": "ml", "defPrice": 0.38, "defDose": "6ml/10l wody"},
    {"name": "Linkomycyna", "unit": "g", "defPrice": 0.56, "defDose": "10mg/kg m.c."},
    {"name": "Enrofloksacyna", "unit": "ml", "defPrice": 0.65, "defDose": "2.5mg/kg m.c."},
    {"name": "Tylozyna", "unit": "g", "defPrice": 0.48, "defDose": "5-10mg/kg m.c."},
    {"name": "Fenbendazol", "unit": "g", "defPrice": 0.72, "defDose": "5mg/kg m.c."},
    {"name": "Ivermektyna", "unit": "ml", "defPrice": 1.20, "defDose": "0.3mg/kg m.c."},
    {"name": "Witaminy AD3E", "unit": "ml", "defPrice": 0.18, "defDose": "1ml/l wody"},
    {"name": "Elektrolity", "unit": "g", "defPrice": 0.12, "defDose": "2g/l wody"},
    {"name": "Inne", "unit": "szt", "defPrice": 0, "defDose": ""},
]

CAUSES = [
    {"name": "APP", "color": "#c62828"},
    {"name": "Beztlen", "color": "#4a148c"},
    {"name": "Krwotoczny", "color": "#b71c1c"},
    {"name": "Wirusówka", "color": "#e65100"},
    {"name": "Przepuklina", "color": "#5d4037"},
    {"name": "Wrzody żołądka", "color": "#bf360c"},
    {"name": "Streptokokoza", "color": "#880e4f"},
    {"name": "Glässer", "color": "#1a237e"},
    {"name": "Dyzenteria", "color": "#004d40"},
    {"name": "Adenomatoza", "color": "#33691e"},
    {"name": "Inne — nieznana", "color": "#616161"},
    {"name": "Inne — wypadek", "color": "#455a64"},
]

FEED_TYPES = ["Starter", "Grower", "Finiszer"]
UBOJNIE = ["Rytel", "Somianka", "Staropolska", "Tetragon", "Zakrzewscy", "Goodvalley", "Skiba"]
BUFORY = ["Pszenżyto", "Jęczmień", "Wysłodki"]

BIOGAZ_CATS = ["silniki", "pompy", "mieszadła", "dozowanie", "inne"]
DOC_CATS = ["dzierżawa", "BDO", "pozwolenie", "ubezpieczenie", "badania", "inne"]
NAWOZ_TYPES = ["Azotowy", "Fosforowy", "Potasowy", "Wieloskładnikowy", "Wapno", "Gnojowica", "Obornik", "Inny"]
OPRYSK_TARGETS = ["Chwasty", "Choroby", "Szkodniki", "Regulator", "Inne"]
PALIWO_TYPES = ["ON", "AdBlue", "Olej hydrauliczny", "Olej silnikowy", "Smar", "Benzyna"]

TODOS_DEF = [
    {"name": "Szczepienie Cirko", "icon": "💉", "cat": "szczepienie", "desc": "PCV2"},
    {"name": "Szczepienie Myko", "icon": "💉", "cat": "szczepienie", "desc": "Mycoplasma hyopneumoniae"},
    {"name": "Szczepienie APP", "icon": "💉", "cat": "szczepienie", "desc": "Actinobacillus pleuropneumoniae"},
    {"name": "Szczepienie Lawsonia", "icon": "💉", "cat": "szczepienie", "desc": "Lawsonia intracellularis"},
    {"name": "Szczepienie PRRS", "icon": "💉", "cat": "szczepienie", "desc": "PRRS — jak najszybciej po wstawieniu"},
    {"name": "Odrobaczanie", "icon": "🔬", "cat": "profilaktyka", "desc": "Panacur / Fenbendazol"},
    {"name": "Dezynfekcja komory", "icon": "🧹", "cat": "higiena", "desc": "Przed wstawieniem"},
    {"name": "Deratyzacja", "icon": "🐀", "cat": "higiena", "desc": "Kontrola gryzoni"},
    {"name": "Przegląd wentylacji", "icon": "🌀", "cat": "technika", "desc": "Sprawdzenie i regulacja"},
    {"name": "Kontrola poideł", "icon": "💧", "cat": "technika", "desc": "Przepływ i czystość"},
    {"name": "Ważenie kontrolne", "icon": "⚖️", "cat": "kontrola", "desc": "Wyrywkowe ważenie"},
]

AKC_DEF = [
    {"nazwa": "GR Janina Potorska", "typ": "Rolnik RR", "col": "#6a1b9a"},
    {"nazwa": "GR Kinga Potorska", "typ": "Rolnik RR", "col": "#c62828"},
    {"nazwa": "GR Mieczysław Potorski", "typ": "VAT", "col": "#1565c0"},
    {"nazwa": "GR Robert Potorski", "typ": "VAT", "col": "#2e7d32"},
]

SILOSY_DEF = [
    {"id": 1, "nazwa": "Silos 1", "poj": 400},
    {"id": 2, "nazwa": "Silos 2", "poj": 400},
    {"id": 3, "nazwa": "Silos 3", "poj": 400},
    {"id": 4, "nazwa": "Silos 4", "poj": 400},
]


def seed():
    db = SessionLocal()
    try:
        # Users
        if db.query(User).count() == 0:
            for u in USERS:
                db.add(User(
                    email=u["email"], name=u["name"],
                    password_hash=hash_password(u["pass"]), role=u["role"]
                ))
            print(f"  ✓ {len(USERS)} użytkowników")

        # Stock (medication inventory)
        if db.query(Stock).count() == 0:
            for m in MEDS:
                db.add(Stock(name=m["name"], unit=m["unit"], qty=0, min_qty=0))
            print(f"  ✓ {len(MEDS)} leków w magazynie")

        # Ubojnie
        if db.query(Ubojnia).count() == 0:
            for name in UBOJNIE:
                db.add(Ubojnia(name=name))
            print(f"  ✓ {len(UBOJNIE)} ubojni")

        # Akcyza
        if db.query(Akcyza).count() == 0:
            for a in AKC_DEF:
                db.add(Akcyza(nazwa=a["nazwa"], typ=a["typ"], col=a["col"], ha=0, swin=0))
            print(f"  ✓ {len(AKC_DEF)} podmiotów akcyzy")

        # Paszarnia (singleton)
        if db.query(Paszarnia).count() == 0:
            db.add(Paszarnia(data={"log": [], "bufory": BUFORY}))
            print("  ✓ Paszarnia")

        # Silosy (singleton)
        if db.query(Silosy).count() == 0:
            db.add(Silosy(data={"silosy": SILOSY_DEF, "log": []}))
            print("  ✓ Silosy")

        # ═══ CUSTOM ELEMENTS (admin-managed lists) ═══
        if db.query(CustomElement).count() == 0:
            count = 0

            # Medications
            for i, m in enumerate(MEDS):
                db.add(CustomElement(
                    category="meds", name=m["name"], unit=m["unit"],
                    def_price=m["defPrice"], def_dose=m["defDose"], sort_order=i
                ))
                count += 1

            # Death causes
            for i, c in enumerate(CAUSES):
                db.add(CustomElement(
                    category="causes", name=c["name"], color=c["color"], sort_order=i
                ))
                count += 1

            # Feed types
            for i, ft in enumerate(FEED_TYPES):
                db.add(CustomElement(category="feed_types", name=ft, sort_order=i))
                count += 1

            # Ubojnie
            for i, u in enumerate(UBOJNIE):
                db.add(CustomElement(category="ubojnie", name=u, sort_order=i))
                count += 1

            # Feed mill buffers
            for i, b in enumerate(BUFORY):
                db.add(CustomElement(category="bufory", name=b, sort_order=i))
                count += 1

            # Biogas categories
            for i, bc in enumerate(BIOGAZ_CATS):
                db.add(CustomElement(category="biogaz_cats", name=bc, sort_order=i))
                count += 1

            # Document categories
            for i, dc in enumerate(DOC_CATS):
                db.add(CustomElement(category="doc_cats", name=dc, sort_order=i))
                count += 1

            # Fertilizer types
            for i, nt in enumerate(NAWOZ_TYPES):
                db.add(CustomElement(category="nawoz_types", name=nt, sort_order=i))
                count += 1

            # Spraying targets
            for i, ot in enumerate(OPRYSK_TARGETS):
                db.add(CustomElement(category="oprysk_targets", name=ot, sort_order=i))
                count += 1

            # Fuel types
            for i, pt in enumerate(PALIWO_TYPES):
                db.add(CustomElement(category="paliwo_types", name=pt, sort_order=i))
                count += 1

            # Default TODO items
            for i, t in enumerate(TODOS_DEF):
                db.add(CustomElement(
                    category="todos_def", name=t["name"], icon=t["icon"],
                    extra={"cat": t["cat"], "desc": t["desc"]}, sort_order=i
                ))
                count += 1

            print(f"  ✓ {count} elementów konfiguracyjnych (admin)")

        db.commit()
        print("  ✓ Seed zakończony")
    except Exception as e:
        db.rollback()
        print(f"  ✗ Błąd seed: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
