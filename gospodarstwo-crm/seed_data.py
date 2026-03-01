"""
Import gruntów z Rejestru Nieruchomości do CRM (tabela grunty).
Uruchom: python seed_grunty.py

Skrypt dodaje 91 działek z pliku Excel do bazy danych CRM.
Przed uruchomieniem upewnij się, że CRM jest skonfigurowany i baza istnieje.
"""
from database import SessionLocal
from models import Grunt

# Mapowanie TERYT -> gmina
GMINA_MAP = {
    "143703_2": "Lubowidz",
    "143703_5": "Lubowidz",
    "143702_2": "Kuczbork-Osada",
    "143706_5": "Żuromin",
}

GRUNTY = [
    {"nr": "419/3", "teryt": "143703_2.0019.419/3", "obreb": "Osówka", "pow": "0.3608", "nazwa": "chlewnia nr 1", "wlasciciel": "Robert Potorski", "kw": "PL2M/00018295/2"},
    {"nr": "419/5", "teryt": "143703_2.0019.419/5", "obreb": "Osówka", "pow": "0.3464", "nazwa": "chlewnia nr 1", "wlasciciel": "Robert Potorski", "kw": "PL2M/00018295/2"},
    {"nr": "419/6", "teryt": "143703_2.0019.419/6", "obreb": "Osówka", "pow": "0.6715", "nazwa": "chlewnia nr 2", "wlasciciel": "Robert Potorski", "kw": "PL2M/00018295/2"},
    {"nr": "419/7", "teryt": "143703_5.0019.419/7", "obreb": "Osówka", "pow": "0.3541", "nazwa": "biogazownia", "wlasciciel": "Robert Potorski", "kw": "PL2M/00018295/2"},
    {"nr": "419/8", "teryt": "143703_5.0019.419/8", "obreb": "Osówka", "pow": "0.4138", "nazwa": "chlewnia nr 2", "wlasciciel": "Robert Potorski", "kw": "PL2M/00018295/2"},
    {"nr": "420/3", "teryt": "143703_2.0019.420/3", "obreb": "Osówka", "pow": "0.6838", "nazwa": "chlewnia nr 3", "wlasciciel": "Robert Potorski", "kw": "PL2M/00023274/7"},
    {"nr": "420/4", "teryt": "143703_2.0019.420/4", "obreb": "Osówka", "pow": "0.3039", "nazwa": "chlewnia nr 3", "wlasciciel": "Robert Potorski", "kw": "PL2M/00023274/7"},
    {"nr": "383/2", "teryt": "143703_2.0019.383/2", "obreb": "Osówka", "pow": "0.3648", "nazwa": 'chlewnia "stara" + magazyn', "wlasciciel": "Robert Potorski", "kw": "PL2M/00022502/8"},
    {"nr": "383/4", "teryt": "143703_2.0019.383/4", "obreb": "Osówka", "pow": "0.0143", "nazwa": "Gospodarstwo", "wlasciciel": "Robert Potorski", "kw": "PL2M/00022502/8"},
    {"nr": "100", "teryt": "143702_2.0021.100", "obreb": "Zielona", "pow": "2.5219", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00013168/8"},
    {"nr": "385/1", "teryt": "143703_5.0019.385/1", "obreb": "Osówka", "pow": "0.5115", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00021112/0"},
    {"nr": "275", "teryt": "143703_5.0019.275", "obreb": "Osówka", "pow": "1.7244", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00021875/6"},
    {"nr": "278", "teryt": "143703_5.0019.278", "obreb": "Osówka", "pow": "4.2259", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00021875/6"},
    {"nr": "292", "teryt": "143703_5.0019.292", "obreb": "Osówka", "pow": "1.2293", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00021875/6"},
    {"nr": "293", "teryt": "143703_5.0019.293", "obreb": "Osówka", "pow": "1.6435", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00021875/6"},
    {"nr": "311", "teryt": "143703_5.0019.311", "obreb": "Osówka", "pow": "1.1415", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00021875/6"},
    {"nr": "51/1", "teryt": "143703_5.0019.51/1", "obreb": "Osówka", "pow": "3.186", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00022502/8"},
    {"nr": "327", "teryt": "143706_5.0023.327", "obreb": "Wiadrowo", "pow": "2.5489", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00022502/8"},
    {"nr": "305", "teryt": "143703_5.0019.305", "obreb": "Osówka", "pow": "2.9971", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00020249/2"},
    {"nr": "306", "teryt": "143703_5.0019.306", "obreb": "Osówka", "pow": "2.1001", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00020249/2"},
    {"nr": "397", "teryt": "143703_5.0019.397", "obreb": "Osówka", "pow": "2.7969", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00018295/2"},
    {"nr": "398", "teryt": "143703_5.0019.398", "obreb": "Osówka", "pow": "1.3746", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00018295/2"},
    {"nr": "385/2", "teryt": "143703_5.0019.385/2", "obreb": "Osówka", "pow": "0.4904", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00018295/2"},
    {"nr": "39", "teryt": "143703_5.0019.39", "obreb": "Osówka", "pow": "3.6574", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00018295/2"},
    {"nr": "384/4", "teryt": "143703_5.0019.384/4", "obreb": "Osówka", "pow": "0.9495", "nazwa": "Grunty orne + panele", "wlasciciel": "Robert Potorski", "kw": "PL2M/00018295/2"},
    {"nr": "421", "teryt": "143703_5.0019.421", "obreb": "Osówka", "pow": "3.5898", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00025112/8"},
    {"nr": "196", "teryt": "143702_2.0021.196", "obreb": "Osówka", "pow": "1.4505", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00024974/1", "uwagi": "UWAGA: obręb w Excel to Osówka, ale TERYT wskazuje na Zielona (143702_2.0021)"},
    {"nr": "138", "teryt": "143702_2.0021.138", "obreb": "Zielona", "pow": "1.3472", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00024903/3"},
    {"nr": "139", "teryt": "143702_2.0021.139", "obreb": "Zielona", "pow": "0.7481", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00024903/3"},
    {"nr": "300/2", "teryt": "143703_5.0019.300/2", "obreb": "Osówka", "pow": "1.4009", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00004230/8"},
    {"nr": "300/1", "teryt": "143703_5.0019.300/1", "obreb": "Osówka", "pow": "0.2997", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00004230/8"},
    {"nr": "3", "teryt": "143703_5.0019.3", "obreb": "Osówka", "pow": "2.5214", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00004230/8"},
    {"nr": "661/2", "teryt": "143703_2.0027.661/2", "obreb": "Straszewy", "pow": "0.9224", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00004230/8"},
    {"nr": "266", "teryt": "143703_5.0019.266", "obreb": "Osówka", "pow": "0.5729", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00003965/2"},
    {"nr": "267/1", "teryt": "143703_2.0019.267/1", "obreb": "Osówka", "pow": "2.3814", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00003965/2"},
    {"nr": "25", "teryt": "143703_5.0037.25", "obreb": "Żelaźnia", "pow": "7.4847", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00003965/2"},
    {"nr": "128", "teryt": "143702_2.0021.128", "obreb": "Zielona", "pow": "1.9241", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00013615/7"},
    {"nr": "126", "teryt": "143702_2.0021.126", "obreb": "Zielona", "pow": "1.4643", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00013615/7"},
    {"nr": "85", "teryt": "143702_2.0021.85", "obreb": "Zielona", "pow": "1.2975", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00013615/7"},
    {"nr": "84", "teryt": "143702_2.0021.84", "obreb": "Zielona", "pow": "1.6979", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00013615/7"},
    {"nr": "68", "teryt": "143703_2.0013.68", "obreb": "Lisiny", "pow": "2.5", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00010047/3"},
    {"nr": "270", "teryt": "143703_5.0019.270", "obreb": "Osówka", "pow": "2.5892", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00024697/5"},
    {"nr": "413", "teryt": "143703_5.0019.413", "obreb": "Osówka", "pow": "2.6327", "nazwa": "Zadrzewione", "wlasciciel": "Robert Potorski", "kw": "PL2M/00024697/5"},
    {"nr": "66", "teryt": "143703_5.0019.66", "obreb": "Osówka", "pow": "1.1908", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00025145/8"},
    {"nr": "128/1", "teryt": "143703_2.0019.128/1", "obreb": "Osówka", "pow": "1.491", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00025145/8"},
    {"nr": "130", "teryt": "143703_5.0019.130", "obreb": "Osówka", "pow": "1.5827", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00025145/8"},
    {"nr": "132/2", "teryt": "143703_2.0019.132/2", "obreb": "Osówka", "pow": "0.5259", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00025145/8"},
    {"nr": "391", "teryt": "143703_5.0019.391", "obreb": "Osówka", "pow": "3.8071", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00025145/8"},
    {"nr": "425", "teryt": "143703_5.0019.425", "obreb": "Osówka", "pow": "1.5553", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00025145/8"},
    {"nr": "392/2", "teryt": "143703_2.0019.392/2", "obreb": "Osówka", "pow": "2.0624", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00026206/1"},
    {"nr": "276", "teryt": "143703_5.0019.276", "obreb": "Osówka", "pow": "1.8173", "nazwa": "Grunty orne", "wlasciciel": "Robert Potorski", "kw": "PL2M/00026407/0"},
    {"nr": "133", "teryt": "143702_2.0019.133", "obreb": "Sarnowo", "pow": "2.4591", "nazwa": "chlewnie Sarnowo", "wlasciciel": "Robert Potorski", "kw": "PL2M/00007567/0"},
    # --- Kinga Potorska ---
    {"nr": "420/5", "teryt": "143703_2.0019.420/5", "obreb": "Osówka", "pow": "0.3777", "nazwa": "chlewnia nr 4", "wlasciciel": "Kinga Potorska", "kw": "PL2M/00023781/4"},
    {"nr": "420/6", "teryt": "143703_2.0019.420/6", "obreb": "Osówka", "pow": "0.3069", "nazwa": "chlewnia nr 4", "wlasciciel": "Kinga Potorska", "kw": "PL2M/00023781/4"},
    {"nr": "388/1", "teryt": "143703_5.0019.388/1", "obreb": "Osówka", "pow": "1.3015", "nazwa": "Grunty orne", "wlasciciel": "Kinga Potorska", "kw": "PL2M/00023443/3"},
    {"nr": "422", "teryt": "143703_5.0019.422", "obreb": "Osówka", "pow": "1.0016", "nazwa": "Grunty orne", "wlasciciel": "Kinga Potorska", "kw": "PL2M/00023443/3"},
    {"nr": "15", "teryt": "143703_5.0019.15", "obreb": "Osówka", "pow": "6.2806", "nazwa": "Grunty orne", "wlasciciel": "Kinga Potorska", "kw": "PL2M/00010826/8"},
    {"nr": "129", "teryt": "143702_2.0015.129", "obreb": "Niedziałki", "pow": "11.76", "nazwa": "Grunty orne", "wlasciciel": "Kinga Potorska", "kw": "PL2M/00020298/0"},
    {"nr": "147", "teryt": "143702_2.0015.147", "obreb": "Niedziałki", "pow": "6.99", "nazwa": "Grunty orne", "wlasciciel": "Kinga Potorska", "kw": "PL2M/00020298/0"},
    {"nr": "149", "teryt": "143702_2.0015.149", "obreb": "Niedziałki", "pow": "2.3", "nazwa": "Grunty orne", "wlasciciel": "Kinga Potorska", "kw": "PL2M/00011747/7"},
    {"nr": "157", "teryt": "143702_2.0015.157", "obreb": "Niedziałki", "pow": "7.23", "nazwa": "Grunty orne", "wlasciciel": "Kinga Potorska", "kw": "PL2M/00011747/7"},
    {"nr": "156", "teryt": "143702_2.0015.156", "obreb": "Niedziałki", "pow": "4.67", "nazwa": "Grunty orne", "wlasciciel": "Kinga Potorska", "kw": "PL2M/00011747/7"},
    {"nr": "155/3", "teryt": "143702_2.0015.155/3", "obreb": "Niedziałki", "pow": "2.4", "nazwa": "Grunty orne", "wlasciciel": "Kinga Potorska", "kw": "PL2M/00011747/7"},
    {"nr": "141", "teryt": "143702_2.0015.141", "obreb": "Niedziałki", "pow": "20.56", "nazwa": "Grunty orne", "wlasciciel": "Kinga Potorska", "kw": "PL2M/00011747/7"},
    {"nr": "153", "teryt": "143702_2.0015.153", "obreb": "Niedziałki", "pow": "17.49", "nazwa": "Grunty orne", "wlasciciel": "Kinga Potorska", "kw": "PL2M/00011747/7"},
    {"nr": "155/1", "teryt": "143702_2.0015.155/1", "obreb": "Niedziałki", "pow": "0.3", "nazwa": "Grunty orne", "wlasciciel": "Kinga Potorska", "kw": "PL2M/00022236/2"},
    # --- Mieczysław Potorski ---
    {"nr": "383/3", "teryt": "143703_2.0019.383/3", "obreb": "Osówka", "pow": "0.4638", "nazwa": "Gospodarstwo", "wlasciciel": "Mieczysław Potorski", "kw": "PL2M/00004722/4"},
    {"nr": "166", "teryt": "143703_5.0019.166", "obreb": "Osówka", "pow": "0.586", "nazwa": "Grunty orne", "wlasciciel": "Mieczysław Potorski", "kw": "PL2M/00004722/4"},
    {"nr": "190", "teryt": "143703_5.0019.190", "obreb": "Osówka", "pow": "2.189", "nazwa": "Grunty orne", "wlasciciel": "Mieczysław Potorski", "kw": "PL2M/00004722/4"},
    {"nr": "363", "teryt": "143703_5.0019.363", "obreb": "Osówka", "pow": "0.5134", "nazwa": "Grunty orne", "wlasciciel": "Mieczysław Potorski", "kw": "PL2M/00004722/4"},
    {"nr": "377", "teryt": "143703_5.0019.377", "obreb": "Osówka", "pow": "2.2056", "nazwa": "Grunty orne", "wlasciciel": "Mieczysław Potorski", "kw": "PL2M/00004722/4"},
    {"nr": "400", "teryt": "143703_5.0019.400", "obreb": "Osówka", "pow": "3.3109", "nazwa": "Grunty orne", "wlasciciel": "Mieczysław Potorski", "kw": "PL2M/00004722/4"},
    {"nr": "204/1", "teryt": "143703_2.0019.204/1", "obreb": "Osówka", "pow": "3.9868", "nazwa": "Grunty orne", "wlasciciel": "Mieczysław Potorski", "kw": "PL2M/00004722/4"},
    {"nr": "204/2", "teryt": "143703_2.0019.204/2", "obreb": "Osówka", "pow": "0.3301", "nazwa": "Grunty orne", "wlasciciel": "Mieczysław Potorski", "kw": "PL2M/00004722/4"},
    {"nr": "272", "teryt": "143703_5.0019.272", "obreb": "Osówka", "pow": "1.6339", "nazwa": "Grunty orne", "wlasciciel": "Mieczysław Potorski", "kw": "PL2M/00008614/2"},
    {"nr": "375", "teryt": "143703_5.0019.375", "obreb": "Osówka", "pow": "4.3152", "nazwa": "Grunty orne", "wlasciciel": "Mieczysław Potorski", "kw": "PL2M/00008614/2"},
    {"nr": "274/2", "teryt": "143703_5.0019.274/2", "obreb": "Osówka", "pow": "2.1496", "nazwa": "Grunty orne", "wlasciciel": "Mieczysław Potorski", "kw": "PL2M/00008614/2"},
    {"nr": "274/1", "teryt": "143703_5.0019.274/1", "obreb": "Osówka", "pow": "0.2261", "nazwa": "Grunty orne", "wlasciciel": "Mieczysław Potorski", "kw": "PL2M/00008614/2"},
    {"nr": "374", "teryt": "143703_5.0019.374", "obreb": "Osówka", "pow": "7.4166", "nazwa": "Grunty orne", "wlasciciel": "Mieczysław Potorski", "kw": "PL2M/00011105/5"},
    {"nr": "205", "teryt": "143703_5.0019.205", "obreb": "Osówka", "pow": "2.3457", "nazwa": "Grunty orne", "wlasciciel": "Mieczysław Potorski", "kw": "PL2M/00011105/5"},
    {"nr": "357/2", "teryt": "143703_5.0019.357/2", "obreb": "Osówka", "pow": "0.1261", "nazwa": "Grunty orne", "wlasciciel": "Mieczysław Potorski", "kw": "PL2M/00011105/5"},
    {"nr": "358", "teryt": "143703_5.0019.358", "obreb": "Osówka", "pow": "0.3765", "nazwa": "Grunty orne", "wlasciciel": "Mieczysław Potorski", "kw": "PL2M/00011105/5"},
    {"nr": "273", "teryt": "143703_5.0019.273", "obreb": "Osówka", "pow": "1.8378", "nazwa": "Grunty orne", "wlasciciel": "Mieczysław Potorski", "kw": "PL2M/00011105/5"},
    {"nr": "430", "teryt": "143703_5.0019.430", "obreb": "Osówka", "pow": "49.2138", "nazwa": "Grunty orne", "wlasciciel": "Mieczysław Potorski", "kw": "PL2M/00012670/3"},
    {"nr": "431", "teryt": "143703_5.0019.431", "obreb": "Osówka", "pow": "1.9075", "nazwa": "Grunty orne", "wlasciciel": "Mieczysław Potorski", "kw": "PL2M/00012670/3"},
    {"nr": "432", "teryt": "143703_5.0019.432", "obreb": "Osówka", "pow": "4.687", "nazwa": "Grunty orne", "wlasciciel": "Mieczysław Potorski", "kw": "PL2M/00012670/3"},
    {"nr": "215", "teryt": "143703_5.0019.215", "obreb": "Osówka", "pow": "1.7063", "nazwa": "Grunty orne", "wlasciciel": "Mieczysław Potorski", "kw": "PL2M/00026199/8"},
    {"nr": "283", "teryt": "143703_5.0019.283", "obreb": "Osówka", "pow": "1.6087", "nazwa": "Grunty orne", "wlasciciel": "Mieczysław Potorski", "kw": "PL2M/00026199/8"},
    {"nr": "412", "teryt": "143703_5.0019.412", "obreb": "Osówka", "pow": "2.7166", "nazwa": "Grunty orne", "wlasciciel": "Mieczysław Potorski", "kw": "PL2M/00026199/8"},
    {"nr": "384/1", "teryt": "143703_5.0019.384/1", "obreb": "Osówka", "pow": "0.1249", "nazwa": "Grunty orne", "wlasciciel": "Mieczysław Potorski", "kw": "PL2M/00026199/8"},
]

WOJ = "mazowieckie"
POWIAT = "żuromiński"


def seed_grunty():
    db = SessionLocal()
    existing = db.query(Grunt).count()
    if existing > 0:
        print(f"⚠️  Tabela grunty zawiera już {existing} rekordów.")
        ans = input("Wyczyścić i załadować na nowo? (t/n): ").strip().lower()
        if ans == "t":
            db.query(Grunt).delete()
            db.commit()
            print("🗑️  Wyczyszczono tabelę grunty.")
        else:
            print("❌ Przerwano import.")
            db.close()
            return

    count = 0
    for g in GRUNTY:
        teryt_prefix = g["teryt"].split(".")[0] if "." in g["teryt"] else ""
        gmina = GMINA_MAP.get(teryt_prefix, "")

        grunt = Grunt(
            nr=g["nr"],
            teryt=g["teryt"],
            obreb=g["obreb"],
            pow=g["pow"],
            gmina=gmina,
            powiat=POWIAT,
            woj=WOJ,
            nazwa=g["nazwa"],
            wlasciciel=g["wlasciciel"],
            kw=g["kw"],
            uwagi=g.get("uwagi", ""),
            obciazona="nie",
            bank_nazwa="",
            bank_kwota="",
        )
        db.add(grunt)
        count += 1

    db.commit()
    db.close()
    print(f"✅ Zaimportowano {count} działek do tabeli grunty.")
    print(f"   Powiat: {POWIAT}, Województwo: {WOJ}")
    print(f"   Gminy: {', '.join(sorted(set(GMINA_MAP.values())))}")


if __name__ == "__main__":
    seed_grunty()
