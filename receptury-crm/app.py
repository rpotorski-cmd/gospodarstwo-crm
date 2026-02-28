"""
KABANEK CRM Receptury — Backend
FastAPI + SQLite + JWT Auth + Role Permissions
"""
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from models import *  # noqa
from seed_data import seed
from routes.auth_routes import router as auth_router
from routes.data_routes import router as data_router

app = FastAPI(title="Kabanek CRM Receptury", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)

# Seed data
from database import SessionLocal
db = SessionLocal()
try:
    seed(db)
finally:
    db.close()

# Routes
app.include_router(auth_router)
app.include_router(data_router)

# Static files
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
async def root():
    return FileResponse(os.path.join(static_dir, "index.html"))


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
