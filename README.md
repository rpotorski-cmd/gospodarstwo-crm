# 🐷 KABANEK — CRM Gospodarstwo

System CRM dla gospodarstwa rolnego Kabanek. Trzy niezależne aplikacje FastAPI + SQLite.

## Aplikacje

| App | Port | Opis |
|-----|------|------|
| [`kabanek-crm`](./kabanek-crm/) | 8000 | CRM klientów, zamówienia, sprzedaż |
| [`gospodarstwo-crm`](./gospodarstwo-crm/) | 8001 | Tuczarnie + Produkcja Roślinna (21 komór, grunty, uprawy, dokumenty) |
| [`receptury-crm`](./receptury-crm/) | 8002 | Receptury paszowe, bilans żywieniowy, normy duńskie |

## Szybki start (lokalnie)

```bash
# 1. Sklonuj repo
git clone https://github.com/rpotorski-cmd/crm-gospodarstwo.git
cd crm-gospodarstwo

# 2. Zainstaluj zależności (wspólne dla wszystkich)
pip install fastapi uvicorn sqlalchemy pydantic python-multipart bcrypt PyJWT

# 3. Uruchom wybraną aplikację
cd kabanek-crm && python app.py       # http://localhost:8000
cd gospodarstwo-crm && python app.py   # http://localhost:8001
cd receptury-crm && python app.py      # http://localhost:8002
```

## Konta

Wszystkie aplikacje: **r.potorski@kabanek.pl** / **Treder02@** (admin)

## Wdrożenie na VPS (OVHcloud)

```bash
# Na serwerze:
cd /opt
git clone https://github.com/rpotorski-cmd/crm-gospodarstwo.git
cd crm-gospodarstwo

# Virtualenv
python3 -m venv venv
source venv/bin/activate
pip install -r kabanek-crm/requirements.txt

# Uruchom wszystkie 3 jako systemd services
sudo cp deploy/kabanek-crm.service /etc/systemd/system/
sudo cp deploy/gospodarstwo-crm.service /etc/systemd/system/
sudo cp deploy/receptury-crm.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now kabanek-crm gospodarstwo-crm receptury-crm
```

## Nginx (reverse proxy)

```nginx
# /etc/nginx/sites-available/kabanek
server {
    listen 80;
    server_name crm.kabanek.pl;

    location /kabanek/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    location /gospodarstwo/ {
        proxy_pass http://127.0.0.1:8001/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    location /receptury/ {
        proxy_pass http://127.0.0.1:8002/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Technologie

- **Backend**: FastAPI + SQLAlchemy + SQLite
- **Auth**: JWT (bcrypt) + role-based permissions
- **Frontend**: Vanilla JS / React (Babel) — serwowany ze static/
