"""
Kabanek CRM - System Zarzadzania Tuczem
Backend: FastAPI + SQLite + JWT Auth
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routes.auth_routes import router as auth_router
from routes.client_routes import router as client_router
from routes.data_routes import router as data_router

app = FastAPI(title="Kabanek CRM", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(auth_router)
app.include_router(client_router)
app.include_router(data_router)

static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.on_event("startup")
async def startup():
    init_db()
    from database import SessionLocal
    from models import User
    db = SessionLocal()
    if not db.query(User).first():
        db.close()
        from seed_data import seed
        seed()
    else:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def root():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Kabanek CRM API</h1><p>Frontend at /static/index.html</p>")

@app.get("/api/health")
async def health():
    return {"status": "ok", "app": "Kabanek CRM", "version": "2.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
