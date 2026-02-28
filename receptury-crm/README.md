# ⚙ KABANEK CRM Receptury — Kombajn Pro

**FastAPI + SQLite + JWT Auth + System uprawnień**

CRM do zarządzania recepturami paszowymi — normy duńskie 30-130 kg.

## Szybki start

```bash
cd receptury-crm
pip install -r requirements.txt
python app.py
```

Otwórz **http://localhost:8001**

## Konto administratora

| Email | Hasło | Rola |
|-------|-------|------|
| r.potorski@kabanek.pl | Treder02@ | **admin** |

Admin może dodać do **3 dodatkowych użytkowników** (limit 4 razem z adminem).

## System uprawnień (3 role)

| Funkcja | Admin | User | Viewer |
|---------|-------|------|--------|
| Dashboard, Bilans | ✅ | ✅ | ✅ |
| Receptury — edycja udziałów | ✅ | ✅ | 👁 |
| Surowce — ceny i wartości | ✅ | ✅ | 👁 |
| Normy żywieniowe | ✅ edycja | 👁 | 👁 |
| Wolumeny produkcji | ✅ edycja | 👁 | 👁 |
| Zarządzanie użytkownikami | ✅ (max 4) | ❌ | ❌ |
| Historia zmian (audit) | ✅ | ❌ | ❌ |

## Moduły

- **Dashboard** — koszty roczne, parametry w normie, struktura kosztów
- **Receptury** — 3 fazy (Starter/Grower/Finiszer), udziały %, normalizacja do 100%
- **Bilans** — porównanie z normami duńskimi, aktywne ograniczenia
- **Surowce** — 27 surowców z cenami i 9 parametrami żywieniowymi
- **Zakupy** — plan zakupów rocznych, budżet
- **Scenariusze** — analiza cenowa, symulacja kwartalna, slider interaktywny
- **Admin** — panel użytkowników, audit log

## API (18 endpointów)

```
POST /api/auth/login            — logowanie
GET  /api/auth/me               — bieżący użytkownik
GET/POST/PUT/DELETE /api/auth/users  — zarządzanie (admin)
GET  /api/auth/audit            — historia zmian (admin)
GET  /api/state                 — cały stan w jednym zapytaniu
GET/POST/PUT/DELETE /api/materials   — surowce
GET/PUT /api/recipes            — receptury
GET/PUT /api/norms              — normy żywieniowe
GET/PUT /api/production         — wolumeny produkcji
```

## Baza danych

SQLite (`receptury_crm.db`) — 6 tabel:
- `users` — użytkownicy z rolami
- `materials` — surowce (27 pozycji)
- `recipes` — receptury 3 faz (JSON shares)
- `norms` — normy duńskie
- `production` — wolumeny roczne
- `audit_log` — historia zmian

## Bezpieczeństwo (produkcja)

1. Zmień `SECRET_KEY` w `config.py`
2. Zmień hasło admina
3. HTTPS (certbot + nginx)
4. Backup `receptury_crm.db`
