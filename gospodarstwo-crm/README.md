# 🐷 Kabanek Gospodarstwo CRM v2.0 — Backend

**FastAPI + SQLite + JWT Auth + 3-rolowy system uprawnień + upload dokumentów**

## Szybki start

```bash
cd gospodarstwo-crm
pip install -r requirements.txt
python app.py
```

Otwórz **http://localhost:8000**

## Konta domyślne

| Email | Hasło | Rola |
|-------|-------|------|
| r.potorski@kabanek.pl | Treder02@ | **admin** (pełny dostęp + użytkownicy max 10) |
| i.staszynska@kabanek.pl | KabanekOsowka | user |
| k.potorska@kabanek.pl | Nowehaslo123 | user |
| zootechnik | osowka | zoo (podgląd tuczarni) |

## Nowe funkcje

### 👥 Zarządzanie użytkownikami (admin)
- Zakładka **Użytkownicy** w Produkcji Roślinnej
- **Limit: max 10 aktywnych użytkowników**
- Dodawanie, edycja ról, zmiana haseł, dezaktywacja/reaktywacja

### 📎 Dokumenty z załącznikami PDF / skany
- Upload PDF, JPG, PNG, WEBP, TIFF, BMP, GIF (max 20 MB)
- Pliki w katalogu `uploads/` na serwerze
- Podgląd/pobieranie przez przeglądarkę
- Workflow: dodaj dokument → zapisz → wgraj plik

## System uprawnień

| Moduł | Admin | User | Zootechnik |
|-------|-------|------|------------|
| Wstawienia (cykle) | ✅ R/W | ✅ R/W | 👁 Read |
| Upadki, leki, ważenia | ✅ R/W | ✅ R/W | ✅ R/W |
| Magazyn, pasza, silosy | ✅ R/W | ✅ R/W | 👁 Read |
| Grunty, uprawy, nawozy | ✅ R/W | ✅ R/W | ❌ |
| Dokumenty + pliki | ✅ R/W + upload | 👁 Read | ❌ |
| Akcyza | ✅ R/W | 👁 Read | ❌ |
| Użytkownicy (max 10) | ✅ | ❌ | ❌ |
| Historia zmian | ✅ | ❌ | ❌ |

## API — 74 endpointy

- `/api/auth/*` — login, users CRUD, audit
- `/api/files/*` — upload/download/delete plików
- `/api/cycles`, `/api/stock`, `/api/feeds`, `/api/paszarnia`, `/api/silosy`, `/api/ubojnie`
- `/api/ciagniki`, `/api/grunty`, `/api/uprawy`, `/api/nawozy`, `/api/opryski`
- `/api/paliwa`, `/api/rdostawy`, `/api/zakupy`, `/api/biogaz`, `/api/dokumenty`, `/api/akcyza`

## Bezpieczeństwo (produkcja)

1. Zmień `SECRET_KEY` w `config.py`
2. Zmień domyślne hasła
3. HTTPS (certbot + nginx)
4. Backup: `uploads/` + `gospodarstwo_crm.db`
