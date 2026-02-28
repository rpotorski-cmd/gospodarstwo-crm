#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# KABANEK CRM — Skrypt wdrożeniowy VPS (Ubuntu/Debian)
# ═══════════════════════════════════════════════════════════════
set -e

echo "🐷 KABANEK CRM — Instalacja"
echo "═══════════════════════════════"

# 1. System packages
echo "📦 Instalacja pakietów..."
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx git

# 2. Clone / pull
if [ -d /opt/crm-gospodarstwo ]; then
    echo "📂 Aktualizacja repozytorium..."
    cd /opt/crm-gospodarstwo
    git pull
else
    echo "📂 Klonowanie repozytorium..."
    sudo git clone https://github.com/rpotorski-cmd/crm-gospodarstwo.git /opt/crm-gospodarstwo
    sudo chown -R $USER:$USER /opt/crm-gospodarstwo
    cd /opt/crm-gospodarstwo
fi

# 3. Virtual environment
echo "🐍 Tworzenie virtualenv..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install fastapi uvicorn sqlalchemy pydantic python-multipart bcrypt PyJWT

# 4. Create upload dirs
mkdir -p gospodarstwo-crm/uploads

# 5. Systemd services
echo "⚙️  Konfiguracja systemd..."
sudo cp deploy/kabanek-crm.service /etc/systemd/system/
sudo cp deploy/gospodarstwo-crm.service /etc/systemd/system/
sudo cp deploy/receptury-crm.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable kabanek-crm gospodarstwo-crm receptury-crm
sudo systemctl restart kabanek-crm gospodarstwo-crm receptury-crm

# 6. Check status
echo ""
echo "✅ Status usług:"
sudo systemctl status kabanek-crm --no-pager -l | head -5
sudo systemctl status gospodarstwo-crm --no-pager -l | head -5
sudo systemctl status receptury-crm --no-pager -l | head -5

echo ""
echo "═══════════════════════════════"
echo "✅ Gotowe!"
echo ""
echo "Aplikacje działają na:"
echo "  🔹 Kabanek CRM:      http://localhost:8000"
echo "  🔹 Gospodarstwo CRM:  http://localhost:8001"
echo "  🔹 Receptury CRM:     http://localhost:8002"
echo ""
echo "Następne kroki:"
echo "  1. Skonfiguruj nginx: sudo nano /etc/nginx/sites-available/kabanek"
echo "  2. Dodaj SSL: sudo certbot --nginx -d crm.kabanek.pl"
echo "  3. Zmień SECRET_KEY w każdym config.py"
echo "  4. Zmień domyślne hasła!"
