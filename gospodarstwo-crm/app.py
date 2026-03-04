from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from database import init_db
from routes import register_routes
from seed_data import seed

app = FastAPI()

# CORS - pozwala na requesty z GitHub Pages
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicjalizacja bazy danych i seed
@app.on_event("startup")
async def startup():
    init_db()
    seed()

# Rejestracja routes
register_routes(app)

# Health check
@app.get("/api/health")
def health():
    return {"success": True, "status": "OK", "database": "connected"}

# Serwowanie statycznych plików (frontend)
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"status": "API działa"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
