import os
import uuid
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import get_db
from models import Dokument, AuditLog, User
from auth import get_current_user, decode_token
from config import can_write, can_read, UPLOAD_DIR, MAX_FILE_SIZE_MB

router = APIRouter(prefix="/api/files", tags=["files"])

ALLOWED_MIME = [
    "application/pdf",
    "image/jpeg", "image/jpg", "image/png", "image/webp", "image/tiff",
    "image/bmp", "image/gif",
]
ALLOWED_EXT = [".pdf", ".jpg", ".jpeg", ".png", ".webp", ".tiff", ".tif", ".bmp", ".gif"]


def audit(db, user, area, action):
    db.add(AuditLog(user_name=user.name, email=user.email, area=area, action=action))
    db.commit()


def get_user_from_token_query(token: str, db: Session) -> User:
    """Resolve user from ?token= query parameter (for browser window.open)"""
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Nieprawidłowy token")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Nieprawidłowy token")
    user = db.query(User).filter(User.id == int(user_id), User.is_active == True).first()
    if not user:
        raise HTTPException(status_code=401, detail="Użytkownik nieaktywny")
    return user


@router.post("/upload/{doc_id}")
async def upload_file(
    doc_id: int,
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload PDF/scan to a document"""
    if not can_write(user.role, "dokumenty"):
        raise HTTPException(status_code=403, detail="Brak uprawnień")

    doc = db.query(Dokument).filter(Dokument.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Dokument nie znaleziony")

    # Validate file type
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ALLOWED_EXT:
        raise HTTPException(status_code=400, detail=f"Niedozwolony typ pliku. Dozwolone: {', '.join(ALLOWED_EXT)}")

    # Read and check size
    content = await file.read()
    size_mb = len(content) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(status_code=400, detail=f"Plik za duży. Maksymalny rozmiar: {MAX_FILE_SIZE_MB} MB")

    # Delete old file if exists
    if doc.file_path and os.path.exists(doc.file_path):
        try:
            os.remove(doc.file_path)
        except OSError:
            pass

    # Save file
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    unique_name = f"{doc_id}_{uuid.uuid4().hex[:8]}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    with open(file_path, "wb") as f:
        f.write(content)

    # Update document record
    doc.file_name = file.filename or unique_name
    doc.file_path = file_path
    doc.file_size = len(content)
    doc.file_mime = file.content_type or "application/octet-stream"
    db.commit()

    audit(db, user, "dokumenty", f"Wgrano plik: {file.filename} → dokument #{doc_id}")

    return {
        "ok": True,
        "fileName": doc.file_name,
        "fileSize": doc.file_size,
        "fileMime": doc.file_mime,
        "url": f"/api/files/download/{doc_id}"
    }


@router.get("/download/{doc_id}")
async def download_file(
    doc_id: int,
    token: str = Query(default=None),
    db: Session = Depends(get_db)
):
    """Download/view document file. Uses ?token= for browser window.open"""
    if not token:
        raise HTTPException(status_code=401, detail="Brak tokena")
    user = get_user_from_token_query(token, db)
    if not can_read(user.role, "dokumenty"):
        raise HTTPException(status_code=403, detail="Brak uprawnień")

    doc = db.query(Dokument).filter(Dokument.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Dokument nie znaleziony")
    if not doc.file_path or not os.path.exists(doc.file_path):
        raise HTTPException(status_code=404, detail="Brak pliku")

    return FileResponse(
        doc.file_path,
        filename=doc.file_name,
        media_type=doc.file_mime or "application/octet-stream"
    )


@router.delete("/delete/{doc_id}")
async def delete_file(
    doc_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete file from document"""
    if not can_write(user.role, "dokumenty"):
        raise HTTPException(status_code=403, detail="Brak uprawnień")

    doc = db.query(Dokument).filter(Dokument.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Dokument nie znaleziony")

    if doc.file_path and os.path.exists(doc.file_path):
        try:
            os.remove(doc.file_path)
        except OSError:
            pass

    old_name = doc.file_name
    doc.file_name = ""
    doc.file_path = ""
    doc.file_size = 0
    doc.file_mime = ""
    db.commit()

    audit(db, user, "dokumenty", f"Usunięto plik: {old_name} z dokumentu #{doc_id}")
    return {"ok": True}
