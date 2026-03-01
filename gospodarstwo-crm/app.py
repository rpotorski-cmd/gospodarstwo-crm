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

# Migration: add file_data column if missing
try:
    from sqlalchemy import text
    with engine.connect() as conn:
        conn.execute(text("ALTER TABLE dokumenty ADD COLUMN IF NOT EXISTS file_data BYTEA"))
        conn.execute(text("ALTER TABLE grunty ADD COLUMN IF NOT EXISTS umowa VARCHAR(255) DEFAULT ''"))
        conn.execute(text("ALTER TABLE grunty ADD COLUMN IF NOT EXISTS termin_umowy VARCHAR(20) DEFAULT ''"))
        conn.execute(text("ALTER TABLE grunty ADD COLUMN IF NOT EXISTS doplaty VARCHAR(100) DEFAULT ''"))
        conn.commit()
        print("  Migration: all columns OK")
except Exception as e:
    print(f"  Migration note: {e}")

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


@app.get("/api/geoportal")
async def geoportal_redirect(teryt: str = ""):
    """Fetch parcel geometry from ULDK, show on Leaflet map with polygon"""
    import urllib.request, urllib.parse, re
    from fastapi.responses import HTMLResponse, RedirectResponse
    if not teryt:
        return RedirectResponse("https://www.google.com/maps")
    coords_js = "[]"
    center_lat, center_lng = 53.168, 19.806
    debug_info = ""
    try:
        url = "https://uldk.gugik.gov.pl/?request=GetParcelById&id=" + teryt + "&result=geom_wkt&srid=4326"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=10)
        txt = resp.read().decode("utf-8", "ignore").strip()
        debug_info = "URL:" + url + " RAW:" + txt[:500].replace("<","&lt;").replace(">","&gt;").replace('"',"'")
        # ULDK returns: "0\nPOLYGON((lng lat, lng lat, ...))" - first line is status
        lines = txt.split("\n")
        wkt = lines[-1].strip() if len(lines) > 1 else txt.strip()
        # Parse POLYGON or MULTIPOLYGON
        ring = re.search(r'\(\(([^)]+)\)', wkt)
        if ring:
            pairs = ring.group(1).split(",")
            coords = []
            for p in pairs:
                parts = p.strip().split()
                if len(parts) >= 2:
                    try:
                        lng, lat = float(parts[0]), float(parts[1])
                        # Sanity check - Poland is roughly lat 49-55, lng 14-24
                        if 14 < lng < 25 and 49 < lat < 55:
                            coords.append([lat, lng])
                    except ValueError:
                        pass
            if coords:
                lats = [c[0] for c in coords]
                lngs = [c[1] for c in coords]
                center_lat = (min(lats) + max(lats)) / 2
                center_lng = (min(lngs) + max(lngs)) / 2
                coords_js = str(coords)
    except Exception as e:
        debug_info = str(e)
    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Działka {teryt}</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>body{{margin:0}}#map{{width:100%;height:100vh}}
.info{{position:absolute;top:10px;left:50px;z-index:1000;background:#fff;padding:8px 16px;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,.3);font:bold 14px sans-serif;color:#1565c0}}</style>
</head><body>
<div class="info">Działka: {teryt}</div>
<div id="map"></div>
<script>
var coords={coords_js};
var map=L.map('map').setView([{center_lat},{center_lng}],17);
L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',{{maxZoom:20,attribution:'OSM'}}).addTo(map);
var dzialki=L.tileLayer.wms('https://integracja.gugik.gov.pl/cgi-bin/KraijObiektServletNew',{{layers:'dzialki,numery_dzialek',format:'image/png',transparent:true,maxZoom:20,attribution:'EGiB'}});
dzialki.addTo(map);
if(coords.length>2){{
  var poly=L.polygon(coords,{{color:'#d32f2f',weight:3,fillColor:'#ff5252',fillOpacity:0.25}}).addTo(map);
  map.fitBounds(poly.getBounds().pad(0.3));
  poly.bindPopup('<b>{teryt}</b>').openPopup();
}}
</script>
<!-- debug: {debug_info} -->
<div style="position:absolute;bottom:5px;left:5px;z-index:1000;background:rgba(255,255,255,0.9);padding:4px 8px;font:10px monospace;max-width:90%;word-break:break-all;border-radius:4px">DEBUG: {debug_info}</div>
</body></html>"""
    return HTMLResponse(html)


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
