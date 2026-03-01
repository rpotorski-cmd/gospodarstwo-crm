import os
import base64
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session
from database import get_db
from models import Dokument, AuditLog, User
from auth import get_current_user, decode_token
from config import can_write, can_read, MAX_FILE_SIZE_MB

router = APIRouter(prefix="/api/files", tags=["files"])

ALLOWED_EXT = [".pdf", ".jpg", ".jpeg", ".png", ".webp", ".tiff", ".tif", ".bmp", ".gif"]


def audit(db, user, area, action):
    db.add(AuditLog(user_name=user.name, email=user.email, area=area, action=action))
    db.commit()


def get_user_from_token_query(token, db):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Nieprawidlowy token")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Nieprawidlowy token")
    user = db.query(User).filter(User.id == int(user_id), User.is_active == True).first()
    if not user:
        raise HTTPException(status_code=401, detail="Uzytkownik nieaktywny")
    return user


@router.post("/upload/{doc_id}")
async def upload_file(
    doc_id: int,
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not can_write(user.role, "dokumenty"):
        raise HTTPException(status_code=403, detail="Brak uprawnien")

    doc = db.query(Dokument).filter(Dokument.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Dokument nie znaleziony")

    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ALLOWED_EXT:
        raise HTTPException(status_code=400, detail=f"Niedozwolony typ pliku. Dozwolone: {', '.join(ALLOWED_EXT)}")

    content = await file.read()
    size_mb = len(content) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(status_code=400, detail=f"Plik za duzy. Max: {MAX_FILE_SIZE_MB} MB")

    # Store file in PostgreSQL
    doc.file_name = file.filename or f"plik{ext}"
    doc.file_data = content
    doc.file_size = len(content)
    doc.file_mime = file.content_type or "application/octet-stream"
    doc.file_path = "db"  # marker that file is in database
    db.commit()

    audit(db, user, "dokumenty", f"Wgrano plik: {file.filename} -> dokument #{doc_id}")

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
    if not token:
        raise HTTPException(status_code=401, detail="Brak tokena")
    user = get_user_from_token_query(token, db)
    if not can_read(user.role, "dokumenty"):
        raise HTTPException(status_code=403, detail="Brak uprawnien")

    doc = db.query(Dokument).filter(Dokument.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Dokument nie znaleziony")
    if not doc.file_data:
        raise HTTPException(status_code=404, detail="Brak pliku")

    return Response(
        content=doc.file_data,
        media_type=doc.file_mime or "application/octet-stream",
        headers={"Content-Disposition": f'inline; filename="{doc.file_name}"'}
    )


@router.delete("/delete/{doc_id}")
async def delete_file(
    doc_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not can_write(user.role, "dokumenty"):
        raise HTTPException(status_code=403, detail="Brak uprawnien")

    doc = db.query(Dokument).filter(Dokument.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Dokument nie znaleziony")

    old_name = doc.file_name
    doc.file_name = ""
    doc.file_path = ""
    doc.file_size = 0
    doc.file_mime = ""
    doc.file_data = None
    db.commit()

    audit(db, user, "dokumenty", f"Usunieto plik: {old_name} z dokumentu #{doc_id}")
    return {"ok": True}
