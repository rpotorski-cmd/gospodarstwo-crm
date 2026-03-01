"""Seed initial data from HTML constants into database"""
from database import SessionLocal
from models import User, Stock, Ubojnia, Akcyza, Paszarnia, Silosy, CustomElement, Grunt, Ciagnik
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





GRUNTY_DATA = [
    {"kw":"PL2M/00018295/2","nr":"419/3","obreb":"Osówka","pow":"0.3608","nazwa":"chlewnia nr 1","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.419/3"},
    {"kw":"PL2M/00018295/2","nr":"419/5","obreb":"Osówka","pow":"0.3464","nazwa":"chlewnia nr 1","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.419/5"},
    {"kw":"PL2M/00018295/2","nr":"419/6","obreb":"Osówka","pow":"0.6715","nazwa":"chlewnia nr 2","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.419/6"},
    {"kw":"PL2M/00018295/2","nr":"419/7","obreb":"Osówka","pow":"0.3541","nazwa":"biogazownia","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.419/7"},
    {"kw":"PL2M/00018295/2","nr":"419/8","obreb":"Osówka","pow":"0.4138","nazwa":"chlewnia nr 2","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.419/8"},
    {"kw":"PL2M/00023274/7","nr":"420/3","obreb":"Osówka","pow":"0.6838","nazwa":"chlewnia nr 3","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.420/3"},
    {"kw":"PL2M/00023274/7","nr":"420/4","obreb":"Osówka","pow":"0.3039","nazwa":"chlewnia nr 3","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.420/4"},
    {"kw":"PL2M/00022502/8","nr":"383/2","obreb":"Osówka","pow":"0.3648","nazwa":"chlewnia \"stara\" + magazyn","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.383/2"},
    {"kw":"PL2M/00022502/8","nr":"383/4","obreb":"Osówka","pow":"0.0143","nazwa":"Gospodarstwo","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.383/4"},
    {"kw":"PL2M/00013168/8","nr":"100","obreb":"Zielona","pow":"2.5219","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Kuczbork-Osada","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143702_2.0021.100"},
    {"kw":"PL2M/00021112/0","nr":"385/1","obreb":"Osówka","pow":"0.5115","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.385/1"},
    {"kw":"PL2M/00021875/6","nr":"275","obreb":"Osówka","pow":"1.7244","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.275"},
    {"kw":"PL2M/00021875/6","nr":"278","obreb":"Osówka","pow":"4.2259","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.278"},
    {"kw":"PL2M/00021875/6","nr":"292","obreb":"Osówka","pow":"1.2293","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.292"},
    {"kw":"PL2M/00021875/6","nr":"293","obreb":"Osówka","pow":"1.6435","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.293"},
    {"kw":"PL2M/00021875/6","nr":"311","obreb":"Osówka","pow":"1.1415","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.311"},
    {"kw":"PL2M/00022502/8","nr":"51/1","obreb":"Osówka","pow":"3.186","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.51/1"},
    {"kw":"PL2M/00022502/8","nr":"327","obreb":"Wiadrowo","pow":"2.5489","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Żuromin","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143706_5.0023.327"},
    {"kw":"PL2M/00020249/2","nr":"305","obreb":"Osówka","pow":"2.9971","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.305"},
    {"kw":"PL2M/00020249/2","nr":"306","obreb":"Osówka","pow":"2.1001","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.306"},
    {"kw":"PL2M/00018295/2","nr":"397","obreb":"Osówka","pow":"2.7969","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.397"},
    {"kw":"PL2M/00018295/2","nr":"398","obreb":"Osówka","pow":"1.3746","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.398"},
    {"kw":"PL2M/00018295/2","nr":"385/2","obreb":"Osówka","pow":"0.4904","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.385/2"},
    {"kw":"PL2M/00018295/2","nr":"39","obreb":"Osówka","pow":"3.6574","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.39"},
    {"kw":"PL2M/00018295/2","nr":"384/4","obreb":"Osówka","pow":"0.9495","nazwa":"Grunty Orne + panele","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.384/4"},
    {"kw":"PL2M/00025112/8","nr":"421","obreb":"Osówka","pow":"3.5898","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.421"},
    {"kw":"PL2M/00024974/1","nr":"196","obreb":"Osówka","pow":"1.4505","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Kuczbork-Osada","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143702_2.0021.196"},
    {"kw":"PL2M/00024903/3","nr":"138","obreb":"Zielona","pow":"1.3472","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Kuczbork-Osada","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143702_2.0021.138"},
    {"kw":"PL2M/00024903/3","nr":"139","obreb":"Zielona","pow":"0.7481","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Kuczbork-Osada","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143702_2.0021.139"},
    {"kw":"PL2M/00004230/8","nr":"300/2","obreb":"Osówka","pow":"1.4009","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.300/2"},
    {"kw":"PL2M/00004230/8","nr":"300/1","obreb":"Osówka","pow":"0.2997","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.300/1"},
    {"kw":"PL2M/00004230/8","nr":"3","obreb":"Osówka","pow":"2.5214","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.3"},
    {"kw":"PL2M/00004230/8","nr":"20","obreb":"Zielona","pow":"4.5447","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Kuczbork-Osada","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143702_2.0021.20"},
    {"kw":"PL2M/00004230/8","nr":"661/2","obreb":"Straszewy","pow":"0.9224","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0027.661/2"},
    {"kw":"PL2M/00003965/2","nr":"266","obreb":"Osówka","pow":"0.5729","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.266"},
    {"kw":"PL2M/00003965/2","nr":"267/1","obreb":"Osówka","pow":"2.3814","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.267/1"},
    {"kw":"PL2M/00003965/2","nr":"25","obreb":"Żelaźnia","pow":"7.4847","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0037.25"},
    {"kw":"PL2M/00013615/7","nr":"128","obreb":"Zielona","pow":"1.9241","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Kuczbork-Osada","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143702_2.0021.128"},
    {"kw":"PL2M/00013615/7","nr":"126","obreb":"Zielona","pow":"1.4643","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Kuczbork-Osada","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143702_2.0021.126"},
    {"kw":"PL2M/00013615/7","nr":"85","obreb":"Zielona","pow":"1.2975","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Kuczbork-Osada","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143702_2.0021.85"},
    {"kw":"PL2M/00013615/7","nr":"84","obreb":"ZIelona","pow":"1.6979","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Kuczbork-Osada","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143702_2.0021.84"},
    {"kw":"PL2M/00010047/3","nr":"68","obreb":"Lisiny","pow":"2.5","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0013.68"},
    {"kw":"PL2M/00024697/5","nr":"270","obreb":"Osówka","pow":"2.5892","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.270"},
    {"kw":"PL2M/00024697/5","nr":"413","obreb":"Osówka","pow":"2.6327","nazwa":"Zadrzewione","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.413"},
    {"kw":"PL2M/00025145/8","nr":"66","obreb":"Osówka","pow":"1.1908","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.66"},
    {"kw":"PL2M/00025145/8","nr":"128/1","obreb":"Osówka","pow":"1.491","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.128/1"},
    {"kw":"PL2M/00025145/8","nr":"130","obreb":"Osówka","pow":"1.5827","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.130"},
    {"kw":"PL2M/00025145/8","nr":"132/2","obreb":"Osówka","pow":"0.5259","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.132/2"},
    {"kw":"PL2M/00025145/8","nr":"391","obreb":"Osówka","pow":"3.8071","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.391"},
    {"kw":"PL2M/00025145/8","nr":"425","obreb":"Osówka","pow":"1.5553","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.425"},
    {"kw":"PL2M/00026206/1","nr":"392/2","obreb":"Osówka","pow":"2.0624","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.392/2"},
    {"kw":"PL2M/00026407/0","nr":"276","obreb":"Osówka","pow":"1.8173","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.276"},
    {"kw":"PL2M/00007567/0","nr":"133","obreb":"Sarnowo","pow":"2.4591","nazwa":"chlewnie Sarnowo","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Kuczbork-Osada","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143702_2.0019.133"},
    {"kw":"PL2M/00023781/4","nr":"420/5","obreb":"Osówka","pow":"0.3777","nazwa":"chlewnia nr 4","wlasciciel":"Kinga Potorska","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.420/5"},
    {"kw":"PL2M/00023781/4","nr":"420/6","obreb":"Osówka","pow":"0.3069","nazwa":"chlewnia nr 4","wlasciciel":"Kinga Potorska","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.420/6"},
    {"kw":"PL2M/00023443/3","nr":"388/1","obreb":"Osówka","pow":"1.3015","nazwa":"Grunty orne","wlasciciel":"Kinga Potorska","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.388/1"},
    {"kw":"PL2M/00023443/3","nr":"422","obreb":"Osówka","pow":"1.0016","nazwa":"Grunty orne","wlasciciel":"Kinga Potorska","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.422"},
    {"kw":"PL2M/00023389/6","nr":"63","obreb":"Lisiny","pow":"2","nazwa":"Grunty orne","wlasciciel":"Kinga Potorska","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0013.63"},
    {"kw":"PL2M/00023379/3","nr":"282","obreb":"Wiadrowo","pow":"2.5601","nazwa":"Grunty orne","wlasciciel":"Kinga Potorska","woj":"mazowieckie","powiat":"żuromiński","gmina":"Żuromin","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143706_5.0023.282"},
    {"kw":"PL2M/00010826/8","nr":"15","obreb":"Osówka","pow":"6.2806","nazwa":"Grunty orne","wlasciciel":"Kinga Potorska","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.15"},
    {"kw":"PL2M/00020298/0","nr":"129","obreb":"Niedziałki","pow":"11.76","nazwa":"Grunty orne","wlasciciel":"Kinga Potorska","woj":"mazowieckie","powiat":"żuromiński","gmina":"Kuczbork-Osada","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143702_2.0015.129"},
    {"kw":"PL2M/00020298/0","nr":"147","obreb":"Niedziałki","pow":"6.99","nazwa":"Grunty orne","wlasciciel":"Kinga Potorska","woj":"mazowieckie","powiat":"żuromiński","gmina":"Kuczbork-Osada","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143702_2.0015.147"},
    {"kw":"PL2M/00011747/7","nr":"149","obreb":"Niedziałki","pow":"2.3","nazwa":"Grunty orne","wlasciciel":"Kinga Potorska","woj":"mazowieckie","powiat":"żuromiński","gmina":"Kuczbork-Osada","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143702_2.0015.149"},
    {"kw":"PL2M/00011747/7","nr":"157","obreb":"Niedziałki","pow":"7.23","nazwa":"Grunty orne","wlasciciel":"Kinga Potorska","woj":"mazowieckie","powiat":"żuromiński","gmina":"Kuczbork-Osada","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143702_2.0015.157"},
    {"kw":"PL2M/00011747/7","nr":"156","obreb":"Niedziałki","pow":"4.67","nazwa":"Grunty orne","wlasciciel":"Kinga Potorska","woj":"mazowieckie","powiat":"żuromiński","gmina":"Kuczbork-Osada","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143702_2.0015.156"},
    {"kw":"PL2M/00011747/7","nr":"155/3","obreb":"Niedziałki","pow":"2.4","nazwa":"Grunty orne","wlasciciel":"Kinga Potorska","woj":"mazowieckie","powiat":"żuromiński","gmina":"Kuczbork-Osada","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143702_2.0015.155/3"},
    {"kw":"PL2M/00011747/7","nr":"141","obreb":"Niedziałki","pow":"20.56","nazwa":"Grunty orne","wlasciciel":"Kinga Potorska","woj":"mazowieckie","powiat":"żuromiński","gmina":"Kuczbork-Osada","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143702_2.0015.141"},
    {"kw":"PL2M/00011747/7","nr":"153","obreb":"Niedziałki","pow":"17.49","nazwa":"Grunty orne","wlasciciel":"Kinga Potorska","woj":"mazowieckie","powiat":"żuromiński","gmina":"Kuczbork-Osada","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143702_2.0015.153"},
    {"kw":"PL2M/00022236/2","nr":"155/1","obreb":"Niedziałki","pow":"0.3","nazwa":"Grunty orne","wlasciciel":"Kinga Potorska","woj":"mazowieckie","powiat":"żuromiński","gmina":"Kuczbork-Osada","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143702_2.0015.155/1"},
    {"kw":"PL2M/00004722/4","nr":"383/3","obreb":"Osówka","pow":"0.4638","nazwa":"Gospodarstwo","wlasciciel":"Mieczysław Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.383/3"},
    {"kw":"PL2M/00004722/4","nr":"166","obreb":"Osówka","pow":"0.586","nazwa":"Grunty orne","wlasciciel":"Mieczysław Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.166"},
    {"kw":"PL2M/00004722/4","nr":"190","obreb":"Osówka","pow":"2.189","nazwa":"Grunty orne","wlasciciel":"Mieczysław Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.190"},
    {"kw":"PL2M/00004722/4","nr":"363","obreb":"Osówka","pow":"0.5134","nazwa":"Grunty orne","wlasciciel":"Mieczysław Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.363"},
    {"kw":"PL2M/00004722/4","nr":"377","obreb":"Osówka","pow":"2.2056","nazwa":"Grunty orne","wlasciciel":"Mieczysław Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.377"},
    {"kw":"PL2M/00004722/4","nr":"400","obreb":"Osówka","pow":"3.3109","nazwa":"Grunty orne","wlasciciel":"Mieczysław Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.400"},
    {"kw":"PL2M/00004722/4","nr":"204/1","obreb":"Osówka","pow":"3.9868","nazwa":"Grunty orne","wlasciciel":"Mieczysław Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.204/1"},
    {"kw":"PL2M/00004722/4","nr":"204/2","obreb":"Osówka","pow":"0.3301","nazwa":"Grunty orne","wlasciciel":"Mieczysław Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.204/2"},
    {"kw":"PL2M/00008614/2","nr":"272","obreb":"Osówka","pow":"1.6339","nazwa":"Grunty orne","wlasciciel":"Mieczysław Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.272"},
    {"kw":"PL2M/00008614/2","nr":"375","obreb":"Osówka","pow":"4.3152","nazwa":"Grunty orne","wlasciciel":"Mieczysław Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.375"},
    {"kw":"PL2M/00008614/2","nr":"274/2","obreb":"Osówka","pow":"2.1496","nazwa":"Grunty orne","wlasciciel":"Mieczysław Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.274/2"},
    {"kw":"PL2M/00008614/2","nr":"274/1","obreb":"Osówka","pow":"0.2261","nazwa":"Grunty orne","wlasciciel":"Mieczysław Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.274/1"},
    {"kw":"PL2M/00011105/5","nr":"374","obreb":"Osówka","pow":"7.4166","nazwa":"Grunty orne","wlasciciel":"Mieczysław Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.374"},
    {"kw":"PL2M/00011105/5","nr":"205","obreb":"Osówka","pow":"2.3457","nazwa":"Grunty orne","wlasciciel":"Mieczysław Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.205"},
    {"kw":"PL2M/00011105/5","nr":"357/2","obreb":"Osówka","pow":"0.1261","nazwa":"Grunty orne","wlasciciel":"Mieczysław Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.357/2"},
    {"kw":"PL2M/00011105/5","nr":"358","obreb":"Osówka","pow":"0.3765","nazwa":"Grunty orne","wlasciciel":"Mieczysław Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.358"},
    {"kw":"PL2M/00011105/5","nr":"273","obreb":"Osówka","pow":"1.8378","nazwa":"Grunty orne","wlasciciel":"Mieczysław Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.273"},
    {"kw":"PL2M/00012670/3","nr":"430","obreb":"Osówka","pow":"49.2138","nazwa":"Grunty orne","wlasciciel":"Mieczysław Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.430"},
    {"kw":"PL2M/00012670/3","nr":"431","obreb":"Osówka","pow":"1.9075","nazwa":"Grunty orne","wlasciciel":"Mieczysław Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.431"},
    {"kw":"PL2M/00012670/3","nr":"432","obreb":"Osówka","pow":"4.687","nazwa":"Grunty orne","wlasciciel":"Mieczysław Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.432"},
    {"kw":"PL2M/00026199/8","nr":"215","obreb":"Osówka","pow":"1.7063","nazwa":"Grunty orne","wlasciciel":"Mieczysław Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.215"},
    {"kw":"PL2M/00026199/8","nr":"283","obreb":"Osówka","pow":"1.6087","nazwa":"Grunty orne","wlasciciel":"Mieczysław Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.283"},
    {"kw":"PL2M/00026199/8","nr":"412","obreb":"Osówka","pow":"2.7166","nazwa":"Grunty orne","wlasciciel":"Mieczysław Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.412"},
    {"kw":"PL2M/00026199/8","nr":"384/1","obreb":"Osówka","pow":"0.1249","nazwa":"Grunty orne","wlasciciel":"Mieczysław Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.384/1"},
    {"kw":"PL2M/00004722/4","nr":"383/3","obreb":"Osówka","pow":"0.4638","nazwa":"Gospodarstwo","wlasciciel":"Mieczysław Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.383/3"},
    {"kw":"NS1Z/00066241/9","nr":"29a/5","obreb":"Kościelisko","pow":"0.0028","nazwa":"Miejsce postojowe nr 1","wlasciciel":"Fundacja Rodzinna","woj":"małopolskie","powiat":"tatrzański","gmina":"Kościelisko","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":""},
    {"kw":"NS1Z/00012350/3","nr":"2958","obreb":"Kościelisko","pow":"0.0876","nazwa":"Mieszkanie nr 1","wlasciciel":"Fundacja Rodzinna","woj":"małopolskie","powiat":"tatrzański","gmina":"Kościelisko","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":""},
    {"kw":"NS1Z/00012350/3","nr":"2958/1","obreb":"Kościelisko","pow":"0.0876","nazwa":"Mieszkanie nr 2","wlasciciel":"Fundacja Rodzinna","woj":"małopolskie","powiat":"tatrzański","gmina":"Kościelisko","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":""},
    {"kw":"NS1Z/00066242/6","nr":"29a/6","obreb":"Kościelisko","pow":"0.0026","nazwa":"Miejsce postojowe nr 2","wlasciciel":"Fundacja Rodzinna","woj":"małopolskie","powiat":"tatrzański","gmina":"Kościelisko","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":""},
]

STOCK_DATA = [
    {"name":"Amoksiklav 500g 62,5%","unit":"szt","qty":5,"note":"AMOKSA"},
    {"name":"Paracilin 1000g","unit":"szt","qty":1,"note":"AMOKSA"},
    {"name":"Fortamox 500mg/g (1000g)","unit":"szt","qty":1,"note":"AMOKSA"},
    {"name":"Biomox 80/100g (1000g)","unit":"szt","qty":6,"note":"AMOKSA"},
    {"name":"Amoxy Active 697mg/g (1kg)","unit":"szt","qty":88,"note":"AMOKSA"},
    {"name":"Octacilin 697mg/g (1kg)","unit":"szt","qty":33,"note":"AMOKSA"},
    {"name":"Doxymed 1000mg/g (1kg) czerwony","unit":"szt","qty":50,"note":"DOKSY"},
    {"name":"Doxymed 500mg/g (5kg) niebieskie","unit":"szt","qty":1,"note":"DOKSY"},
    {"name":"Altidox 500mg/g (1kg)","unit":"szt","qty":20,"note":"DOKSY"},
    {"name":"Lincoscan 400mg/g (1,5kg)","unit":"szt","qty":1,"note":"LINKOMYCYNA"},
    {"name":"Dophalin 1kg","unit":"szt","qty":23,"note":"LINKOMYCYNA"},
    {"name":"Lincofort 400 (1500g)","unit":"szt","qty":4,"note":"LINKOMYCYNA"},
    {"name":"Solutyl 1,1kg","unit":"szt","qty":1,"note":"TYLOZYNA"},
    {"name":"Tylogran","unit":"szt","qty":149,"note":"TYLOZYNA"},
    {"name":"Enrofloksacyna Vetos-Farma 100mg/ml (1L)","unit":"szt","qty":31,"note":"ENROFLOKSACYNA"},
    {"name":"Enrobioflox 10% 100mg/ml (1000ml)","unit":"szt","qty":2,"note":"ENROFLOKSACYNA"},
    {"name":"Aquacoli 2000000 j.m./ml (5ml)","unit":"szt","qty":12,"note":"KOLISTYNY SIARCZAN"},
    {"name":"Nipoxyme 22.500.000 IU/g (250g)","unit":"szt","qty":8,"note":"KOLISTYNY SIARCZAN"},
    {"name":"Coldostin 4 800 000 IU/g (1kg)","unit":"szt","qty":1,"note":"KOLISTYNY SIARCZAN"},
    {"name":"Colfive 5 000 000 j.m./ml (5L)","unit":"szt","qty":3,"note":"KOLISTYNY SIARCZAN"},
    {"name":"Aivlosin 625mg/g (5x400g)","unit":"kartoniki","qty":31,"note":"155 paczek łącznie"},
    {"name":"Neofort 700mg/g (1000g)","unit":"szt","qty":67,"note":"NEOMYCYNY SIARCZAN"},
    {"name":"Neomycyna Vetos Farma 1000g","unit":"szt","qty":36,"note":"NEOMYCYNY SIARCZAN"},
    {"name":"Neosol 145g/1000ml (900ml)","unit":"szt","qty":6,"note":"NEOMYCYNY SIARCZAN"},
    {"name":"Ecomectin 6mg/g (5x333g)","unit":"paczki","qty":71,"note":"IWERMYKTYNA"},
    {"name":"Lewamizol 10% 100mg/g (1000g)","unit":"szt","qty":12,"note":"LEWAMIZOLU CHLOROWODOREK"},
    {"name":"Levamol 8% (800g)","unit":"szt","qty":1,"note":"LEWAMIZOLU CHLOROWODOREK"},
    {"name":"Panacur Aquasol 200mg/ml (4L)","unit":"szt","qty":2,"note":"LEWAMIZOLU CHLOROWODOREK"},
    {"name":"Floron 100mg/ml (~1L)","unit":"szt","qty":3,"note":"FLORFENIKOL"},
    {"name":"K-FLOR 100mg/ml (1L)","unit":"szt","qty":13,"note":"FLORFENIKOL"},
    {"name":"Hypersol 500mg/g (5kg)","unit":"szt","qty":2,"note":"OKSYTETRACYKLINA"},
    {"name":"Oksytetracyklina 50% (500g)","unit":"szt","qty":1,"note":"OKSYTETRACYKLINA"},
    {"name":"Fenbenat 40mg/g (500g)","unit":"szt","qty":4,"note":"FENBENAT"},
    {"name":"Solacyl 1000mg/g (1kg)","unit":"szt","qty":1,"note":"SODU SALICYLAN"},
    {"name":"Tilmovet 100mg/g (1kg)","unit":"szt","qty":4,"note":"TYLMIKOZYNA"},
    {"name":"Tildosin 250mg/ml (960ml)","unit":"szt","qty":1,"note":"TYLMIKOZYNA"},
    {"name":"Vetmulin 450mg/g (1kg)","unit":"szt","qty":26,"note":"TIAMULINA"},
    {"name":"Biomutin 450mg/g (1kg)","unit":"szt","qty":8,"note":"TIAMULINA"},
    {"name":"Metaxol 20/100mg/ml (5L)","unit":"szt","qty":1,"note":"SULFAMETOKSAZOL"},
    {"name":"Metasol 1kg","unit":"szt","qty":30,"note":"ROZPUSZCZALNIK AMOKSY"},
    {"name":"Węglan sodu bezwodny","unit":"szt","qty":10,"note":"ROZPUSZCZALNIK AMOKSY"},
    {"name":"Magi 960g","unit":"szt","qty":25,"note":"DODATKI / WITAMINY"},
    {"name":"Garlic Stroong 5L","unit":"szt","qty":1,"note":"napoczęte"},
    {"name":"Eselin 5L","unit":"szt","qty":11,"note":"DODATKI / WITAMINY"},
    {"name":"Vit K 5L","unit":"szt","qty":9,"note":"DODATKI / WITAMINY"},
    {"name":"Vit C 25kg","unit":"szt","qty":3,"note":"DODATKI / WITAMINY"},
    {"name":"Nervomix 5L","unit":"szt","qty":1,"note":"DODATKI / WITAMINY"},
    {"name":"AD3E + K3 5L","unit":"szt","qty":1,"note":"DODATKI / WITAMINY"},
    {"name":"Pulmomix AERO 5L","unit":"szt","qty":3,"note":"1 szt używana"},
    {"name":"Ossi forte 5L","unit":"szt","qty":6,"note":"DODATKI / WITAMINY"},
    {"name":"Vit N 5L","unit":"szt","qty":36,"note":"DODATKI / WITAMINY"},
]

CIAGNIKI_DATA = [
    {"typ":"ciagnik","nazwa":"CF MOTO C-FORCE 625S","marka":"CF MOTO","rok":"2024","rejestr":"WP9238","uwagi":"Rodzaj: ciągnik rolniczy | VIN: LCELDUZP8R6000749 | Poj: 580 ccm | Właściciel: ING LEASE (POLSKA) sp. z o.o. o/w Płocku | Ubezpieczający: Kabanek Sp. z o.o."},
    {"typ":"ciagnik","nazwa":"CLAAS AXION 850","marka":"CLAAS","rok":"2023","rejestr":"WE721C","uwagi":"Rodzaj: ciągnik rolniczy | VIN: VPKTA6000A5002027 | Poj: 6728 ccm | Właściciel: ING LEASE (POLSKA) sp. z o.o. | Ubezpieczający: Kabanek Sp. z o.o."},
    {"typ":"ciagnik","nazwa":"MASSEY FERGUSON MF 7600","marka":"MASSEY FERGUSON","rok":"2012","rejestr":"WZUNV99","uwagi":"Rodzaj: ciągnik rolniczy | VIN: C282074 | Poj: 7365 ccm | Właściciel: Robert Potorski | Ubezpieczający: Robert Potorski"},
    {"typ":"ciagnik","nazwa":"MASSEY FERGUSON MF 8730","marka":"MASSEY FERGUSON","rok":"2020","rejestr":"WP7560","uwagi":"Rodzaj: ciągnik rolniczy | VIN: VKKMY45GLLB293059 | Poj: 8419 ccm | Właściciel: Kabanek Sp. z o.o. | Ubezpieczający: Kabanek Sp. z o.o."},
    {"typ":"ciagnik","nazwa":"MTZ 1221A","marka":"MTZ","rok":"2006","rejestr":"WZUT722","uwagi":"Rodzaj: ciągnik rolniczy | VIN: 00479M | Poj: 7120 ccm | Właściciel: Mieczysław Potorski | Ubezpieczający: Mieczysław Potorski"},
    {"typ":"ciagnik","nazwa":"MTZ BELARUS 1221.2","marka":"MTZ","rok":"2018","rejestr":"WZUTP71","uwagi":"Rodzaj: ciągnik rolniczy | VIN: Y4R122101J1101167 | Poj: 7120 ccm | Właściciel: Robert Potorski | Ubezpieczający: Robert Potorski"},
    {"typ":"ciagnik","nazwa":"MTZ BELARUS TRAKTOR 1025A","marka":"MTZ","rok":"2001","rejestr":"WZUN080","uwagi":"Rodzaj: ciągnik rolniczy | VIN: 00108R | Poj: 4752 ccm | Właściciel: Kinga Potorska | Ubezpieczający: Kinga Potorska"},
    {"typ":"ciagnik","nazwa":"NEW HOLLAND T6050","marka":"NEW HOLLAND","rok":"2009","rejestr":"WZUNJ15","uwagi":"Rodzaj: ciągnik rolniczy | VIN: Z9BD04696 | Poj: 6728 ccm | Właściciel: Robert Potorski | Ubezpieczający: Robert Potorski"},
    {"typ":"ciagnik","nazwa":"NEW HOLLAND T7.200","marka":"NEW HOLLAND","rok":"2015","rejestr":"WZUTG98","uwagi":"Rodzaj: ciągnik rolniczy | VIN: ZFBN10434 | Poj: 6728 ccm | Właściciel: Robert Potorski | Ubezpieczający: Robert Potorski"},
    {"typ":"ciagnik","nazwa":"RENAULT T 480 T 4x2","marka":"RENAULT","rok":"2022","rejestr":"WGM8958L","uwagi":"Rodzaj: ciągnik siodłowy | VIN: VF611A36XND038612 | Poj: 12777 ccm | Właściciel: PKO Leasing S.A. | Ubezpieczający: Kabanek Sp. z o.o."},
    {"typ":"ciagnik","nazwa":"SCANIA S 500 A4x2NA Highline","marka":"SCANIA","rok":"2024","rejestr":"WGM7253L","uwagi":"Rodzaj: ciągnik siodłowy | VIN: YS2S4X20005760172 | Poj: 12742 ccm | Właściciel: PKO Leasing S.A. | Ubezpieczający: Kabanek Sp. z o.o."},
    {"typ":"ciagnik","nazwa":"SCANIA S 500 A4x2NA Highline","marka":"SCANIA","rok":"2024","rejestr":"WGM7251L","uwagi":"Rodzaj: ciągnik siodłowy | VIN: YS2S4X20005759893 | Poj: 12742 ccm | Właściciel: PKO Leasing S.A. | Ubezpieczający: Kabanek Sp. z o.o."},
    {"typ":"ciagnik","nazwa":"SCANIA S 500 A4x2NA Highline","marka":"SCANIA","rok":"2024","rejestr":"WGM2399M","uwagi":"Rodzaj: ciągnik siodłowy | VIN: YS2S4X20005770032 | Poj: 12742 ccm | Właściciel: PKO Leasing S.A. | Ubezpieczający: Kabanek Sp. z o.o."},
    {"typ":"ciagnik","nazwa":"SCANIA S 500 B6x2NA Highline","marka":"SCANIA","rok":"2024","rejestr":"WGM7250L","uwagi":"Rodzaj: ciągnik siodłowy | VIN: YS2S4X20005759912 | Poj: 12742 ccm | Właściciel: PKO Leasing S.A. | Ubezpieczający: Kabanek Sp. z o.o."},
    {"typ":"ciagnik","nazwa":"SCANIA S 500 B6x2NA Highline","marka":"SCANIA","rok":"2025","rejestr":"WGM2398M","uwagi":"Rodzaj: ciągnik siodłowy | VIN: YS2S4X20005770058 | Poj: 12742 ccm | Właściciel: PKO Leasing S.A. | Ubezpieczający: Kabanek Sp. z o.o."},
    {"typ":"ladowarka","nazwa":"KMM M630-60","marka":"KMM","rok":"2019","rejestr":"---","uwagi":"Rodzaj: ładowarka teleskopowa | VIN: 630012 | Właściciel: Kabanek Sp. z o.o. | Ubezpieczający: Kabanek Sp. z o.o."},
    {"typ":"inne","nazwa":"BRANDYS PS 217.13","marka":"BRANDYS","rok":"1990","rejestr":"WZUS766","uwagi":"Rodzaj: przyczepa ciężarowa, wywrotka | VIN: TKYPS1721L2002969 | Właściciel: Mieczysław Potorski | Ubezpieczający: Mieczysław Potorski"},
    {"typ":"inne","nazwa":"DACIA DUSTER 1.5 DCI LAUREATE 4X4","marka":"DACIA","rok":"2015","rejestr":"WZU96RC","uwagi":"Rodzaj: osobowy | VIN: UU1HSDJ9G53719660 | Poj: 1461 ccm | Właściciel: Kinga Potorska | Ubezpieczający: Kinga Potorska"},
    {"typ":"inne","nazwa":"KASSBOHRER SSL 35","marka":"KASSBOHRER","rok":"2007","rejestr":"WZU518AC","uwagi":"Rodzaj: naczepa ciężarowa, pojemnik, przewóz towarów sypkich | VIN: WKV67233471350378 | Właściciel: Gospodarstwo Rolne Robert Potorski | Ubezpieczający: Robert Potorski"},
    {"typ":"inne","nazwa":"KIA SPORTAGE 1.6 T-GDI MR`19 E6D","marka":"KIA","rok":"2021","rejestr":"WND99416","uwagi":"Rodzaj: osobowy | VIN: U5YPG816GML041445 | Poj: 1591 ccm | Właściciel: Kabanek Sp. z o.o. | Ubezpieczający: Kabanek Sp. z o.o."},
    {"typ":"inne","nazwa":"KIA STONIC 1.0 T-GDI M DCT","marka":"KIA","rok":"2020","rejestr":"WP7540N","uwagi":"Rodzaj: osobowy | VIN: KNADA817GM6481395 | Poj: 998 ccm | Właściciel: Natural-Pig Sp. z o.o. | Ubezpieczający: Natural-Pig Sp. z o.o."},
    {"typ":"inne","nazwa":"LEXUS RX 22-","marka":"LEXUS","rok":"2023","rejestr":"WP6073S","uwagi":"Rodzaj: osobowy | VIN: JTJCMBHA902008285 | Poj: 2393 ccm | Właściciel: ING LEASE (POLSKA) sp. z o.o. o/w Płocku | Ubezpieczający: Kabanek Sp. z o.o."},
    {"typ":"inne","nazwa":"LEXUS RX500H","marka":"LEXUS","rok":"2023","rejestr":"WP1809S","uwagi":"Rodzaj: osobowy | VIN: JTJCMBHA202005034 | Poj: 2393 ccm | Właściciel: ING LEASE (POLSKA) sp. z o.o. o/w Płocku | Ubezpieczający: Kabanek Sp. z o.o."},
    {"typ":"inne","nazwa":"MAN TGM","marka":"MAN","rok":"2007","rejestr":"NO3928T","uwagi":"Rodzaj: ciężarowy | VIN: WMAN26ZZX8Y205376 | Poj: 6871 ccm | Właściciel: Kabanek Sp. z o.o. | Ubezpieczający: Kabanek Sp. z o.o."},
    {"typ":"inne","nazwa":"PEZZAIOLI SBA31","marka":"PEZZAIOLI","rok":"2024","rejestr":"WGM9083R","uwagi":"Rodzaj: naczepa ciężarowa, inna, przewóz żywych zwierząt | VIN: ZFJSBA31URM008705 | Właściciel: PKO Leasing S.A. | Ubezpieczający: Kabanek Sp. z o.o."},
    {"typ":"inne","nazwa":"PEZZAIOLI SBA31","marka":"PEZZAIOLI","rok":"2024","rejestr":"WGM9231R","uwagi":"Rodzaj: naczepa ciężarowa, inna, przewóz żywych zwierząt | VIN: ZFJSBA31URM008706 | Właściciel: PKO Leasing S.A. | Ubezpieczający: Kabanek Sp. z o.o."},
    {"typ":"inne","nazwa":"PEZZAIOLI SBA31","marka":"PEZZAIOLI","rok":"2024","rejestr":"WGM9284R","uwagi":"Rodzaj: naczepa ciężarowa, inna, przewóz żywych zwierząt | VIN: ZFJSBA31URM008707 | Właściciel: PKO Leasing S.A. | Ubezpieczający: Kabanek Sp. z o.o."},
    {"typ":"inne","nazwa":"PEZZAIOLI SBA31","marka":"PEZZAIOLI","rok":"2025","rejestr":"WGM0010S","uwagi":"Rodzaj: naczepa ciężarowa, inna, przewóz żywych zwierząt | VIN: ZFJSBA31URM008713 | Właściciel: PKO Leasing S.A. | Ubezpieczający: Kabanek Sp. z o.o."},
    {"typ":"inne","nazwa":"PEZZAIOLI SBA32","marka":"PEZZAIOLI","rok":"2024","rejestr":"WGM8874R","uwagi":"Rodzaj: naczepa ciężarowa, inna, przewóz żywych zwierząt | VIN: ZFJSBA31URM008682 | Właściciel: ING LEASE (POLSKA) sp. z o.o. | Ubezpieczający: Kabanek Sp. z o.o."},
    {"typ":"inne","nazwa":"PEZZAIOLI SBA63/S F138AL","marka":"PEZZAIOLI","rok":"2023","rejestr":"WGM3161R","uwagi":"Rodzaj: naczepa ciężarowa, inna, przewóz żywych zwierząt | VIN: ZFJSBA63UPM008291 | Właściciel: ING LEASE (POLSKA) sp. z o.o. | Ubezpieczający: Kabanek Sp. z o.o."},
    {"typ":"inne","nazwa":"PORSCHE MACAN T","marka":"PORSCHE","rok":"2022","rejestr":"WD2652R","uwagi":"Rodzaj: osobowy | VIN: WP1ZZZ950PLB08674 | Poj: 1984 ccm | Właściciel: SANTANDER CONSUMER MULTIRENT sp. z o.o. | Ubezpieczający: Kabanek Sp. z o.o."},
    {"typ":"inne","nazwa":"PRONAR T 672/2","marka":"PRONAR","rok":"2009","rejestr":"WZUPE44","uwagi":"Rodzaj: przyczepa ciężarowa rolnicza, skrzynia | VIN: SZB6722XX91X00151 | Właściciel: Robert Potorski | Ubezpieczający: Robert Potorski"},
    {"typ":"inne","nazwa":"PRONAR T700XL","marka":"PRONAR","rok":"2019","rejestr":"WZUSR35","uwagi":"Rodzaj: przyczepa ciężarowa | VIN: SZB700XLXK2X00105 | Właściciel: Robert Potorski | Ubezpieczający: Robert Potorski"},
    {"typ":"inne","nazwa":"SAM SAM","marka":"SAM","rok":"1992","rejestr":"WZUP436","uwagi":"Rodzaj: przyczepa lekka | VIN: CI2700415 | Właściciel: Janina Potorska | Ubezpieczający: Janina Potorska"},
    {"typ":"inne","nazwa":"SKODA FELICIA 98-01","marka":"SKODA","rok":"2001","rejestr":"WCI44XC","uwagi":"Rodzaj: osobowy | VIN: TMBEFF6131X353115 | Poj: 1289 ccm | Właściciel: Mieczysław Potorski | Ubezpieczający: Mieczysław Potorski"},
    {"typ":"inne","nazwa":"SUZUKI Vitara 1.5 DualJet Hybrid Premium Plus 4WD AGS","marka":"SUZUKI","rok":"2024","rejestr":"WP1648T","uwagi":"Rodzaj: osobowy | VIN: TSMLYEH1S00D63837 | Poj: 1462 ccm | Właściciel: ING LEASE (POLSKA) sp. z o.o. o/w Płocku | Ubezpieczający: Natural-Pig Sp. z o.o."},
    {"typ":"inne","nazwa":"SUZUKI Vitara 1.5 Strong Hybrid Elegance Sun 4WD AGS","marka":"SUZUKI","rok":"2024","rejestr":"WP1825T","uwagi":"Rodzaj: osobowy | VIN: TSMLYEH1S00D62489 | Poj: 1462 ccm | Właściciel: ING LEASE (POLSKA) sp. z o.o. o/w Płocku | Ubezpieczający: Natural-Pig Sp. z o.o."},
    {"typ":"inne","nazwa":"SUZUKI Vitara 1.5 Strong Hybrid Premium 2WD AGS","marka":"SUZUKI","rok":"2024","rejestr":"WP2419T","uwagi":"Rodzaj: osobowy | VIN: TSMLYEH1S00D78589 | Poj: 1462 ccm | Właściciel: ING LEASE (POLSKA) sp. z o.o. o/w Płocku | Ubezpieczający: Natural-Pig Sp. z o.o."},
    {"typ":"inne","nazwa":"TOYOTA Proace City","marka":"TOYOTA","rok":"2021","rejestr":"WP9108P","uwagi":"Rodzaj: ciężarowy | VIN: YAREFYHYCGJ972231 | Poj: 1499 ccm | Właściciel: Toyota Leasing Polska Sp. z o.o. o/w Płocku | Ubezpieczający: Natural-Pig Sp. z o.o."},
    {"typ":"inne","nazwa":"TOYOTA RAV4 2.5 Hybrid Selection 4x2","marka":"TOYOTA","rok":"2021","rejestr":"WP8337P","uwagi":"Rodzaj: osobowy | VIN: JTMGBRFV20D072942 | Poj: 2487 ccm | Właściciel: ING LEASE (POLSKA) sp. z o.o. o/w Płocku | Ubezpieczający: Kabanek Sp. z o.o."},
    {"typ":"inne","nazwa":"TOYOTA RAV4 2.5 Hybrid Selection 4x4","marka":"TOYOTA","rok":"2024","rejestr":"WP7805S","uwagi":"Rodzaj: osobowy | VIN: JTME63FV50D557813 | Poj: 2487 ccm | Właściciel: ING LEASE (POLSKA) sp. z o.o. o/w Płocku | Ubezpieczający: Kabanek Sp. z o.o."},
    {"typ":"inne","nazwa":"TOYOTA RAV4 2.5 Hybrid Selection 4x4","marka":"TOYOTA","rok":"2024","rejestr":"WE8CL09","uwagi":"Rodzaj: osobowy | VIN: JTME63FVX0J048947 | Poj: 2487 ccm | Właściciel: ING LEASE (POLSKA) sp. z o.o. | Ubezpieczający: Kabanek Sp. z o.o."},
    {"typ":"inne","nazwa":"TOYOTA RAV4 2.5 Plug-In Hybrid Selection 4x4","marka":"TOYOTA","rok":"2024","rejestr":"WP7874S","uwagi":"Rodzaj: osobowy | VIN: JTME63FV60D557951 | Poj: 2487 ccm | Właściciel: ING LEASE (POLSKA) sp. z o.o. o/w Płocku | Ubezpieczający: Kabanek Sp. z o.o."},
    {"typ":"inne","nazwa":"VOLVO FM","marka":"VOLVO","rok":"2015","rejestr":"WZU6FF5","uwagi":"Rodzaj: ciężarowy, pojemnik, przewóz sypkich artykułów spożywczych | VIN: YV2XTW0C4FB715529 | Poj: 12777 ccm | Właściciel: Natural-Pig Sp. z o.o. | Ubezpieczający: Natural-Pig Sp. z o.o."},
    {"typ":"inne","nazwa":"WIELTON PRS-2/W10","marka":"WIELTON","rok":"2010","rejestr":"WZUPG82","uwagi":"Rodzaj: przyczepa ciężarowa rolnicza, wywrotka | VIN: SUDPRS20000020978 | Właściciel: Robert Potorski | Ubezpieczający: Robert Potorski"},
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

        # Stock (medication inventory) - reseed from Excel import
        existing_stock = db.query(Stock).count()
        has_old_stock = existing_stock > 0 and existing_stock < len(STOCK_DATA)
        if existing_stock == 0 or has_old_stock:
            if has_old_stock:
                db.query(Stock).delete()
                print("  ↻ Aktualizacja magazynu leków z Excela")
            for s in STOCK_DATA:
                db.add(Stock(name=s["name"], unit=s["unit"], qty=s["qty"], min_qty=0, note=s.get("note","")))
            print(f"  ✓ {len(STOCK_DATA)} leków zaimportowanych z Excela")

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


        # Ciagniki/Maszyny (z Excela pojazdów) - reseed if empty or fewer
        existing_ciag = db.query(Ciagnik).count()
        if existing_ciag == 0 or existing_ciag < len(CIAGNIKI_DATA):
            if existing_ciag > 0:
                db.query(Ciagnik).delete()
                print("  ↻ Aktualizacja maszyn z wykazu pojazdów")
            for c in CIAGNIKI_DATA:
                db.add(Ciagnik(
                    typ=c["typ"], nazwa=c["nazwa"], marka=c["marka"],
                    rok=c["rok"], rejestr=c["rejestr"], uwagi=c["uwagi"]
                ))
            print(f"  ✓ {len(CIAGNIKI_DATA)} maszyn/pojazdów zaimportowanych")

        # Grunty (z Excela) - reseed if old data
        existing_grunty = db.query(Grunt).count()
        has_old = existing_grunty > 0 and (
            db.query(Grunt).filter(Grunt.woj == "warminsko-mazurskie").first() is not None
            or db.query(Grunt).filter(Grunt.gmina == "").first() is not None
            or db.query(Grunt).filter(Grunt.powiat == "").first() is not None
            or db.query(Grunt).filter(Grunt.gmina == "Kisielice").first() is not None
            or db.query(Grunt).filter(Grunt.gmina == "Iława").first() is not None
            or db.query(Grunt).filter(Grunt.powiat == "iławski").first() is not None
            or db.query(Grunt).filter(Grunt.woj == "warmińsko-mazurskie").first() is not None
        )
        if existing_grunty == 0 or has_old:
            if has_old:
                db.query(Grunt).delete()
                print("  ↻ Czyszczenie starych gruntów")
            for g in GRUNTY_DATA:
                db.add(Grunt(
                    kw=g["kw"], nr=g["nr"], obreb=g["obreb"], pow=g["pow"],
                    nazwa=g["nazwa"], wlasciciel=g["wlasciciel"],
                    woj=g.get("woj",""), powiat=g.get("powiat",""), gmina=g.get("gmina",""),
                    umowa=g.get("umowa",""), termin_umowy=g.get("termin_umowy",""),
                    doplaty=g.get("doplaty",""), uwagi=g["uwagi"], teryt=g["teryt"]
                ))
            print(f"  ✓ {len(GRUNTY_DATA)} działek z rejestru")

        db.commit()
        print("  ✓ Seed zakończony")
    except Exception as e:
        db.rollback()
        print(f"  ✗ Błąd seed: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
