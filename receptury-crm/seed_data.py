import json
from sqlalchemy.orm import Session
from models import User, Material, Recipe, Norm, Production
from auth import hash_password


DEFAULT_MATERIALS = [
    {"name": "Kukurydza", "price": 780, "protein": 8.5, "ne": 10.2, "lys": 0.23, "met": 0.17, "thr": 0.26, "trp": 0.06, "fiber": 2.2, "calcium": 8.5, "phosphorus": 0.08},
    {"name": "Pszenica", "price": 830, "protein": 11.5, "ne": 9.8, "lys": 0.27, "met": 0.18, "thr": 0.3, "trp": 0.09, "fiber": 2.5, "calcium": 9, "phosphorus": 0.1},
    {"name": "Jęczmień", "price": 770, "protein": 10.5, "ne": 8.7, "lys": 0.25, "met": 0.16, "thr": 0.28, "trp": 0.08, "fiber": 4.5, "calcium": 18, "phosphorus": 0.11},
    {"name": "Śruta sojowa 46%", "price": 1550, "protein": 46, "ne": 9.0, "lys": 2.65, "met": 0.6, "thr": 1.7, "trp": 0.58, "fiber": 3.3, "calcium": 11.5, "phosphorus": 0.65},
    {"name": "Śruta rzepakowa", "price": 975, "protein": 34, "ne": 7.5, "lys": 1.7, "met": 0.55, "thr": 1.25, "trp": 0.38, "fiber": 11.5, "calcium": 30, "phosphorus": 0.45},
    {"name": "DDGS", "price": 1100, "protein": 30, "ne": 8.2, "lys": 0.8, "met": 0.5, "thr": 0.9, "trp": 0.22, "fiber": 8, "calcium": 28, "phosphorus": 0.3},
    {"name": "Mączka mięsno-kostna", "price": 1250, "protein": 48, "ne": 7.2, "lys": 2.8, "met": 0.85, "thr": 1.6, "trp": 0.4, "fiber": 0, "calcium": 0, "phosphorus": 3.5},
    {"name": "Suszona krew", "price": 2350, "protein": 85, "ne": 8.0, "lys": 7.5, "met": 1.2, "thr": 3.8, "trp": 1.1, "fiber": 0, "calcium": 0, "phosphorus": 0.25},
    {"name": "Wysłodki suche", "price": 960, "protein": 10, "ne": 7.0, "lys": 0.45, "met": 0.15, "thr": 0.4, "trp": 0.08, "fiber": 18, "calcium": 45, "phosphorus": 0.1},
    {"name": "Olej sojowy", "price": 4900, "protein": 0, "ne": 26.0, "lys": 0, "met": 0, "thr": 0, "trp": 0, "fiber": 0, "calcium": 0, "phosphorus": 0},
    {"name": "Lizyna HCL", "price": 8000, "protein": 0, "ne": 0, "lys": 78, "met": 0, "thr": 0, "trp": 0, "fiber": 0, "calcium": 0, "phosphorus": 0},
    {"name": "DL-Metionina", "price": 12000, "protein": 0, "ne": 0, "lys": 0, "met": 99, "thr": 0, "trp": 0, "fiber": 0, "calcium": 0, "phosphorus": 0},
    {"name": "L-Treonina", "price": 9000, "protein": 0, "ne": 0, "lys": 0, "met": 0, "thr": 98, "trp": 0, "fiber": 0, "calcium": 0, "phosphorus": 0},
    {"name": "L-Tryptofan", "price": 15000, "protein": 0, "ne": 0, "lys": 0, "met": 0, "thr": 0, "trp": 98, "fiber": 0, "calcium": 0, "phosphorus": 0},
    {"name": "Kreda", "price": 400, "protein": 0, "ne": 0, "lys": 0, "met": 0, "thr": 0, "trp": 0, "fiber": 0, "calcium": 38, "phosphorus": 0},
    {"name": "Fosforan MCP", "price": 3000, "protein": 0, "ne": 0, "lys": 0, "met": 0, "thr": 0, "trp": 0, "fiber": 0, "calcium": 16, "phosphorus": 22},
    {"name": "Sól", "price": 1000, "protein": 0, "ne": 0, "lys": 0, "met": 0, "thr": 0, "trp": 0, "fiber": 0, "calcium": 0, "phosphorus": 0},
    {"name": "Premiks 2.5%", "price": 2500, "protein": 0, "ne": 0, "lys": 0, "met": 0, "thr": 0, "trp": 0, "fiber": 0, "calcium": 20, "phosphorus": 5},
    {"name": "Pszenżyto", "price": 700, "protein": 10.5, "ne": 9.5, "lys": 0.3, "met": 0.2, "thr": 0.33, "trp": 0.09, "fiber": 2.8, "calcium": 10.5, "phosphorus": 0.12},
    {"name": "Łuska sojowa", "price": 800, "protein": 12, "ne": 6.0, "lys": 0.6, "met": 0.2, "thr": 0.5, "trp": 0.1, "fiber": 35, "calcium": 60, "phosphorus": 0.15},
    {"name": "Otręba jaglana", "price": 590, "protein": 12, "ne": 7.5, "lys": 0.45, "met": 0.18, "thr": 0.55, "trp": 0.12, "fiber": 19, "calcium": 25, "phosphorus": 0.3},
    {"name": "Zakwaszacz", "price": 7500, "protein": 0, "ne": 0, "lys": 0, "met": 0, "thr": 0, "trp": 0, "fiber": 0, "calcium": 0, "phosphorus": 0},
    {"name": "Premiks MPUM 3%", "price": 4000, "protein": 0, "ne": 0, "lys": 12.5, "met": 4.6, "thr": 5.5, "trp": 1.3, "fiber": 0, "calcium": 10, "phosphorus": 1},
    {"name": "Żyto", "price": 650, "protein": 7.5, "ne": 8.8, "lys": 0.22, "met": 0.16, "thr": 0.25, "trp": 0.07, "fiber": 2.5, "calcium": 13, "phosphorus": 0.11},
    {"name": "Sorgo", "price": 890, "protein": 10.5, "ne": 9.5, "lys": 0.24, "met": 0.18, "thr": 0.27, "trp": 0.08, "fiber": 2, "calcium": 9, "phosphorus": 0.1},
    {"name": "ImmunoWall", "price": 11000, "protein": 0, "ne": 0, "lys": 0, "met": 0, "thr": 0, "trp": 0, "fiber": 0, "calcium": 0, "phosphorus": 0},
    {"name": "Mycofix® 5", "price": 15000, "protein": 0, "ne": 0, "lys": 0, "met": 0, "thr": 0, "trp": 0, "fiber": 0, "calcium": 0, "phosphorus": 0},
]

DEFAULT_RECIPES = {
    "Starter": [2.9, 29.57, 12, 3.5, 0, 0, 6, 2.5, 3, 1, 0, 0, 0, 0, 0, 0, 0.1, 0, 32.03, 0, 4, 0.1, 3, 0, 0, 0.1, 0.2],
    "Grower": [5.5, 15, 11.5, 2.5, 0, 0, 7.7, 1.5, 3.5, 0.9, 0, 0, 0, 0, 0, 0, 0.1, 0, 26.8, 0, 7, 0.1, 3, 14.65, 0, 0.1, 0.15],
    "Finiszer": [7, 9, 11.5, 2, 0, 0, 7.5, 0.5, 3.5, 0.6, 0, 0, 0, 0, 0, 0, 0.1, 0, 28.2, 0, 9, 0.1, 3, 17.75, 0, 0.1, 0.15],
}

DEFAULT_NORMS = {
    "Starter": {"protein": 16.7, "ne": 9.8, "lys": 1.05, "met": 0.60, "thr": 0.68, "trp": 0.21, "fiber": 4.5, "calcium": 0.70, "phosphorus": 0.36},
    "Grower": {"protein": 15.5, "ne": 10.0, "lys": 0.88, "met": 0.52, "thr": 0.60, "trp": 0.19, "fiber": 5.0, "calcium": 0.65, "phosphorus": 0.32},
    "Finiszer": {"protein": 14.4, "ne": 10.2, "lys": 0.72, "met": 0.45, "thr": 0.52, "trp": 0.17, "fiber": 6.0, "calcium": 0.60, "phosphorus": 0.28},
}

DEFAULT_PRODUCTION = {"Starter": 3000, "Grower": 6000, "Finiszer": 6000}


def seed(db: Session):
    # Admin user
    if not db.query(User).first():
        db.add(User(
            email="r.potorski@kabanek.pl",
            name="Rafał Potorski",
            password_hash=hash_password("Treder02@"),
            role="admin"
        ))
        db.commit()

    # Materials
    if not db.query(Material).first():
        for i, m in enumerate(DEFAULT_MATERIALS):
            db.add(Material(sort_order=i, **m))
        db.commit()

    # Recipes
    if not db.query(Recipe).first():
        for phase, shares in DEFAULT_RECIPES.items():
            db.add(Recipe(phase=phase, shares=json.dumps(shares)))
        db.commit()

    # Norms
    if not db.query(Norm).first():
        for phase, vals in DEFAULT_NORMS.items():
            db.add(Norm(phase=phase, **vals))
        db.commit()

    # Production
    if not db.query(Production).first():
        for phase, vol in DEFAULT_PRODUCTION.items():
            db.add(Production(phase=phase, volume=vol))
        db.commit()
