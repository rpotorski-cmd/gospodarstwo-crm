"""
Kabanek Gospodarstwo CRM — Backend
FastAPI + SQLite + JWT Auth + 3-Role Permissions
"""
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from models import *  # noqa: ensure all models registered
from seed_data import seed
from routes.auth_routes import router as auth_router
from routes.tuczarnie_routes import router as tucz_router
from routes.roslinna_routes import router as rosl_router
from routes.admin_routes import router as admin_router
from routes.files_routes import router as files_router
from config import MODULE_PERMS, UPLOAD_DIR

app = FastAPI(title="Kabanek Gospodarstwo CRM", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)

# Seed default data on first run
print("Sprawdzanie danych poczatkowych...")
seed()

# Routes
app.include_router(auth_router)
app.include_router(tucz_router)
app.include_router(rosl_router)
app.include_router(admin_router)
app.include_router(files_router)

# Create upload directory
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/api/permissions")
async def get_permissions():
    return MODULE_PERMS


@app.get("/")
async def root():
    index = os.path.join(static_dir, "index.html")
    if os.path.exists(index):
        return FileResponse(index)
    return JSONResponse({"status": "Kabanek Gospodarstwo CRM API", "docs": "/docs"})


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
