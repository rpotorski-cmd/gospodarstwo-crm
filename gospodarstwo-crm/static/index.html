"""Seed initial data from HTML constants into database"""
from database import SessionLocal
from models import User, Stock, Ubojnia, Akcyza, Paszarnia, Silosy, CustomElement, Grunt
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
    {"kw":"PL2M/00018295/2","nr":"419/3","obreb":"Osówka","pow":"0.3608","nazwa":"chlewnia nr 1","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_2.0019.419/3"},
    {"kw":"PL2M/00018295/2","nr":"419/5","obreb":"Osówka","pow":"0.3464","nazwa":"chlewnia nr 1","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_2.0019.419/5"},
    {"kw":"PL2M/00018295/2","nr":"419/6","obreb":"Osówka","pow":"0.6715","nazwa":"chlewnia nr 2","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_2.0019.419/6"},
    {"kw":"PL2M/00018295/2","nr":"419/7","obreb":"Osówka","pow":"0.3541","nazwa":"biogazownia","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.419/7"},
    {"kw":"PL2M/00018295/2","nr":"419/8","obreb":"Osówka","pow":"0.4138","nazwa":"chlewnia nr 2","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.419/8"},
    {"kw":"PL2M/00023274/7","nr":"420/3","obreb":"Osówka","pow":"0.6838","nazwa":"chlewnia nr 3","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_2.0019.420/4"},
    {"kw":"PL2M/00023274/7","nr":"420/4","obreb":"Osówka","pow":"0.3039","nazwa":"chlewnia nr 3","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_2.0019.420/3"},
    {"kw":"PL2M/00022502/8","nr":"383/2","obreb":"Osówka","pow":"0.3648","nazwa":"chlewnia \"stara\" + magazyn","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_2.0019.383/2"},
    {"kw":"PL2M/00022502/8","nr":"383/4","obreb":"Osówka","pow":"0.0143","nazwa":"Gospodarstwo","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_2.0019.383/4"},
    {"kw":"PL2M/00013168/8","nr":"100","obreb":"Zielona","pow":"2.5219","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Kuczbork-Osada","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143702_2.0021.100"},
    {"kw":"PL2M/00021112/0","nr":"385/1","obreb":"Osówka","pow":"0.5115","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.385/1"},
    {"kw":"PL2M/00021875/6","nr":"275","obreb":"Osówka","pow":"1.7244","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.275"},
    {"kw":"PL2M/00021875/6","nr":"278","obreb":"Osówka","pow":"4.2259","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.278"},
    {"kw":"PL2M/00021875/6","nr":"292","obreb":"Osówka","pow":"1.2293","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.292"},
    {"kw":"PL2M/00021875/6","nr":"293","obreb":"Osówka","pow":"1.6435","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.293"},
    {"kw":"PL2M/00021875/6","nr":"311","obreb":"Osówka","pow":"1.1415","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.311"},
    {"kw":"PL2M/00022502/8","nr":"51/1","obreb":"Osówka","pow":"3.186","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.51/1"},
    {"kw":"PL2M/00022502/8","nr":"327","obreb":"Wiadrowo","pow":"2.5489","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Żuromin","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143706_5.0023.327"},
    {"kw":"PL2M/00020249/2","nr":"305","obreb":"Osówka","pow":"2.9971","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.306"},
    {"kw":"PL2M/00020249/2","nr":"306","obreb":"Osówka","pow":"2.1001","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.305"},
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
    {"kw":"PL2M/00004230/8","nr":"20","obreb":"Zielona","pow":"4.5447","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Kuczbork-Osada","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":""},
    {"kw":"PL2M/00004230/8","nr":"661/2","obreb":"Straszewy","pow":"0.9224","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_2.0027.661/2"},
    {"kw":"PL2M/00003965/2","nr":"266;","obreb":"Osówka","pow":"0.5729","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.266"},
    {"kw":"PL2M/00003965/2","nr":"267/1","obreb":"Osówka","pow":"2.3814","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_2.0019.267/1"},
    {"kw":"PL2M/00003965/2","nr":"25","obreb":"Żelaźnia","pow":"7.4847","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0037.25"},
    {"kw":"PL2M/00013615/7","nr":"128","obreb":"Zielona","pow":"1.9241","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Kuczbork-Osada","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143702_2.0021.128"},
    {"kw":"PL2M/00013615/7","nr":"126","obreb":"Zielona","pow":"1.4643","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Kuczbork-Osada","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143702_2.0021.126"},
    {"kw":"PL2M/00013615/7","nr":"85","obreb":"Zielona","pow":"1.2975","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Kuczbork-Osada","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143702_2.0021.85"},
    {"kw":"PL2M/00013615/7","nr":"84","obreb":"ZIelona","pow":"1.6979","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Kuczbork-Osada","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143702_2.0021.84"},
    {"kw":"PL2M/00010047/3","nr":"68","obreb":"Lisiny","pow":"2.5","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_2.0013.68"},
    {"kw":"PL2M/00024697/5","nr":"270","obreb":"Osówka","pow":"2.5892","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.270"},
    {"kw":"PL2M/00024697/5","nr":"413","obreb":"Osówka","pow":"2.6327","nazwa":"Zadrzewione","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.413"},
    {"kw":"PL2M/00025145/8","nr":"66","obreb":"Osówka","pow":"1.1908","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.66"},
    {"kw":"PL2M/00025145/8","nr":"128/1","obreb":"Osówka","pow":"1.491","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_2.0019.128/1"},
    {"kw":"PL2M/00025145/8","nr":"130","obreb":"Osówka","pow":"1.5827","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.130"},
    {"kw":"PL2M/00025145/8","nr":"132/2","obreb":"Osówka","pow":"0.5259","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_2.0019.132/2"},
    {"kw":"PL2M/00025145/8","nr":"391","obreb":"Osówka","pow":"3.8071","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.391"},
    {"kw":"PL2M/00025145/8","nr":"425","obreb":"Osówka","pow":"1.5553","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.425"},
    {"kw":"PL2M/00026206/1","nr":"392/2","obreb":"Osówka","pow":"2.0624","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_2.0019.392/2"},
    {"kw":"PL2M/00026407/0","nr":"276","obreb":"Osówka","pow":"1.8173","nazwa":"Grunty orne","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.276"},
    {"kw":"PL2M/00007567/0","nr":"133","obreb":"Sarnowo","pow":"2.4591","nazwa":"chlewnie Sarnowo","wlasciciel":"Robert Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Kuczbork-Osada","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143702_2.0019.133"},
    {"kw":"PL2M/00023781/4","nr":"420/5","obreb":"Osówka","pow":"0.3777","nazwa":"chlewnia nr 4","wlasciciel":"Kinga Potorska","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_2.0019.420/5"},
    {"kw":"PL2M/00023781/4","nr":"420/6","obreb":"Osówka","pow":"0.3069","nazwa":"chlewnia nr 4","wlasciciel":"Kinga Potorska","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_2.0019.420/6"},
    {"kw":"PL2M/00023443/3","nr":"388/1","obreb":"Osówka","pow":"1.3015","nazwa":"Grunty orne","wlasciciel":"Kinga Potorska","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.388/1"},
    {"kw":"PL2M/00023443/3","nr":"422","obreb":"Osówka","pow":"1.0016","nazwa":"Grunty orne","wlasciciel":"Kinga Potorska","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.422"},
    {"kw":"PL2M/00023389/6","nr":"63","obreb":"Lisiny","pow":"2","nazwa":"Grunty orne","wlasciciel":"Kinga Potorska","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":""},
    {"kw":"PL2M/00023379/3","nr":"282","obreb":"Wiadrowo","pow":"2.5601","nazwa":"Grunty orne","wlasciciel":"Kinga Potorska","woj":"mazowieckie","powiat":"żuromiński","gmina":"Żuromin","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":""},
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
    {"kw":"PL2M/00004722/4","nr":"383/3","obreb":"Osówka","pow":"0.4638","nazwa":"Gospodarstwo","wlasciciel":"Mieczysław Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_2.0019.383/3"},
    {"kw":"PL2M/00004722/4","nr":"166","obreb":"Osówka","pow":"0.586","nazwa":"Grunty orne","wlasciciel":"Mieczysław Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.166"},
    {"kw":"PL2M/00004722/4","nr":"190","obreb":"Osówka","pow":"2.189","nazwa":"Grunty orne","wlasciciel":"Mieczysław Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.190"},
    {"kw":"PL2M/00004722/4","nr":"363","obreb":"Osówka","pow":"0.5134","nazwa":"Grunty orne","wlasciciel":"Mieczysław Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.363"},
    {"kw":"PL2M/00004722/4","nr":"377","obreb":"Osówka","pow":"2.2056","nazwa":"Grunty orne","wlasciciel":"Mieczysław Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.377"},
    {"kw":"PL2M/00004722/4","nr":"400","obreb":"Osówka","pow":"3.3109","nazwa":"Grunty orne","wlasciciel":"Mieczysław Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_5.0019.400"},
    {"kw":"PL2M/00004722/4","nr":"204/1","obreb":"Osówka","pow":"3.9868","nazwa":"Grunty orne","wlasciciel":"Mieczysław Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_2.0019.204/1"},
    {"kw":"PL2M/00004722/4","nr":"204/2","obreb":"Osówka","pow":"0.3301","nazwa":"Grunty orne","wlasciciel":"Mieczysław Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_2.0019.204/2"},
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
    {"kw":"PL2M/00004722/4","nr":"383/3","obreb":"Osówka","pow":"0.4638","nazwa":"Gospodarstwo","wlasciciel":"Mieczysław Potorski","woj":"mazowieckie","powiat":"żuromiński","gmina":"Lubowidz","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":"143703_2.0019.383/3"},
    {"kw":"NS1Z/00066241/9","nr":"29a/5","obreb":"Kościelisko","pow":"0.0028","nazwa":"Miejsce postojowe nr 1","wlasciciel":"Fundacja Rodzinna","woj":"małopolskie","powiat":"tatrzański","gmina":"Kościelisko","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":""},
    {"kw":"NS1Z/00012350/3","nr":"2958","obreb":"Kościelisko","pow":"0.0876","nazwa":"Mieszkanie nr 1","wlasciciel":"Fundacja Rodzinna","woj":"małopolskie","powiat":"tatrzański","gmina":"Kościelisko","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":""},
    {"kw":"NS1Z/00012350/3","nr":"2958/1","obreb":"Kościelisko","pow":"0.0876","nazwa":"Mieszkanie nr 2","wlasciciel":"Fundacja Rodzinna","woj":"małopolskie","powiat":"tatrzański","gmina":"Kościelisko","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":""},
    {"kw":"NS1Z/00066242/6","nr":"29a/6","obreb":"Kościelisko","pow":"0.0026","nazwa":"Miejsce postojowe nr 2","wlasciciel":"Fundacja Rodzinna","woj":"małopolskie","powiat":"tatrzański","gmina":"Kościelisko","umowa":"","termin_umowy":"","doplaty":"","uwagi":"","teryt":""},
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


        # Grunty (z Excela) - reseed if old data
        existing_grunty = db.query(Grunt).count()
        has_old = existing_grunty > 0 and (
            db.query(Grunt).filter(Grunt.woj == "warminsko-mazurskie").first() is not None
            or db.query(Grunt).filter(Grunt.gmina == "").first() is not None
            or db.query(Grunt).filter(Grunt.powiat == "").first() is not None
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
