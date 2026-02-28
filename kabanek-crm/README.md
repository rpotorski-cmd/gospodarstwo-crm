# 🐷 Kabanek CRM v2.0 — System Zarządzania Tuczem

Pełna aplikacja webowa z bazą danych, autoryzacją JWT i systemem uprawnień.

## Stack technologiczny

| Warstwa | Technologia |
|---------|------------|
| Backend | Python 3.10+ / FastAPI |
| Baza danych | SQLite (SQLAlchemy ORM) |
| Autoryzacja | JWT (python-jose + bcrypt) |
| Frontend | Vanilla JS + Chart.js + CSS3 |

## Szybki start

```bash
# 1. Zainstaluj zależności
pip install -r requirements.txt

# 2. Uruchom serwer (baza i dane testowe utworzą się automatycznie)
python app.py

# 3. Otwórz w przeglądarce
# http://localhost:8000
```

## Konta domyślne

| Login | Hasło | Rola |
|-------|-------|------|
| `admin` | `admin123` | Administrator |
| `manager` | `manager123` | Manager |
| `pracownik` | `prac123` | Pracownik |

> ⚠️ Zmień hasła w środowisku produkcyjnym!

## System uprawnień (3 role)

### 👑 Administrator
- Pełny CRUD na wszystkich danych
- Zarządzanie użytkownikami (tworzenie, edycja, dezaktywacja)
- Przypisywanie klientów do pracowników
- Podgląd logów aktywności
- Eksport danych

### 📋 Manager
- Podgląd wszystkich danych
- Dodawanie i edycja klientów, cykli, finansów
- Brak zarządzania użytkownikami
- Brak usuwania rekordów

### 👷 Pracownik
- Podgląd **tylko przypisanych** klientów
- Dodawanie nowych cykli tuczu
- Brak edycji/usuwania
- Brak zarządzania użytkownikami

## Struktura bazy danych

```
users              — konta użytkowników
clients            — klienci (hodowcy)
client_assignments — przypisanie pracownik ↔ klient
cycle_records      — cykle tuczu
feed_monthly       — dane miesięczne dostawców pasz
finance_records    — rekordy finansowe
yearly_stats       — statystyki roczne
feed_suppliers     — dostawcy pasz (katalog)
activity_logs      — logi aktywności
```

## Endpointy API

### Autoryzacja
- `POST /api/auth/login` — logowanie
- `GET /api/auth/me` — aktualny użytkownik
- `GET /api/auth/users` — lista użytkowników (admin)
- `POST /api/auth/users` — nowy użytkownik (admin)
- `PUT /api/auth/users/{id}` — edycja (admin)
- `DELETE /api/auth/users/{id}` — dezaktywacja (admin)

### Klienci
- `GET /api/clients` — lista (filtrowanie, presets)
- `GET /api/clients/{id}` — szczegóły
- `POST /api/clients` — dodaj
- `PUT /api/clients/{id}` — edytuj
- `DELETE /api/clients/{id}` — usuń (soft delete)
- `POST /api/clients/assign` — przypisz klienta do pracownika

### Cykle tuczu
- `GET /api/cycles` — lista cykli
- `POST /api/cycles` — nowy cykl
- `PUT /api/cycles/{id}` — edycja
- `DELETE /api/cycles/{id}` — usunięcie

### Dashboard & Dane
- `GET /api/dashboard` — dane dashboardu
- `GET /api/feed` — dane dostawców pasz
- `GET /api/finance` — dane finansowe
- `GET /api/activity` — logi aktywności

### Inne
- `GET /api/health` — status serwera
- `GET /api/permissions` — uprawnienia aktualnego użytkownika

## Produkcja

Dla wdrożenia produkcyjnego:

1. Zmień `SECRET_KEY` w `config.py`
2. Zmień domyślne hasła
3. Rozważ PostgreSQL zamiast SQLite
4. Dodaj HTTPS (np. nginx reverse proxy)
5. Ustaw `CORS` na konkretną domenę

```bash
# Uruchomienie produkcyjne
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```
