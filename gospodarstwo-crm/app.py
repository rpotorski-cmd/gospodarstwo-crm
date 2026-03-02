"""
Kabanek Gospodarstwo CRM - Backend
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
from routes.bioasekuracja_routes import router as bio_router
from config import MODULE_PERMS, UPLOAD_DIR

app = FastAPI(title="Kabanek Gospodarstwo CRM", version="2.0")

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse


class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        proto = request.headers.get("x-forwarded-proto", "https")
        if proto == "http" and os.getenv("RAILWAY_ENVIRONMENT"):
            url = request.url.replace(scheme="https")
            return RedirectResponse(url=str(url), status_code=301)
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        if os.getenv("RAILWAY_ENVIRONMENT"):
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response


app.add_middleware(SecurityMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        os.getenv("ALLOWED_ORIGIN", "https://gospodarstwo-crm-production.up.railway.app"),
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)

# Migration: add columns if missing
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
app.include_router(bio_router)

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
    import urllib.request, urllib.parse, re
    from fastapi.responses import HTMLResponse, RedirectResponse
    if not teryt:
        return RedirectResponse("https://www.google.com/maps")
    teryts = [t.strip() for t in teryt.split(",") if t.strip()]
    all_polygons = []
    center_lat, center_lng = 53.168, 19.806
    debug_info = ""
    all_lats, all_lngs = [], []
    for single_teryt in teryts:
        try:
            url = "https://uldk.gugik.gov.pl/?request=GetParcelById&id=" + single_teryt + "&result=geom_wkt&srid=4326"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            resp = urllib.request.urlopen(req, timeout=10)
            txt = resp.read().decode("utf-8", "ignore").strip()
            debug_info += single_teryt + ":" + txt[:150].replace("<", "&lt;").replace(">", "&gt;").replace('"', "'") + " | "
            lines = txt.split("\n")
            wkt = lines[-1].strip() if len(lines) > 1 else txt.strip()
            ring = re.search(r'\(\(([^)]+)\)', wkt)
            if ring:
                pairs = ring.group(1).split(",")
                coords = []
                for p in pairs:
                    parts = p.strip().split()
                    if len(parts) >= 2:
                        try:
                            lng, lat = float(parts[0]), float(parts[1])
                            if 14 < lng < 25 and 49 < lat < 55:
                                coords.append([lat, lng])
                                all_lats.append(lat)
                                all_lngs.append(lng)
                        except ValueError:
                            pass
                if coords:
                    nr = single_teryt.split(".")[-1] if "." in single_teryt else single_teryt
                    all_polygons.append({"teryt": single_teryt, "nr": nr, "coords": coords})
        except Exception as e:
            debug_info += single_teryt + ":ERR:" + str(e) + " | "
    if all_lats:
        center_lat = (min(all_lats) + max(all_lats)) / 2
        center_lng = (min(all_lngs) + max(all_lngs)) / 2
    polygons_js = str([{"teryt": p["teryt"], "nr": p["nr"], "coords": p["coords"]} for p in all_polygons]).replace("'", '"')
    title = ", ".join(teryts) if len(teryts) <= 3 else f"{len(teryts)} dzialek"
    colors = ["#ff1744", "#2979ff", "#00e676", "#ff9100", "#d500f9", "#00e5ff", "#ffea00", "#ff6d00"]
    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Mapa: {title}</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
body{{margin:0;font-family:Arial,sans-serif}}
#map{{width:100%;height:100vh}}
.info-panel{{position:absolute;top:12px;left:55px;z-index:1000;background:rgba(255,255,255,0.95);padding:10px 18px;border-radius:10px;box-shadow:0 4px 20px rgba(0,0,0,.35);max-width:400px}}
.info-panel h3{{margin:0 0 4px;font-size:14px;color:#1a3328}}
.info-panel .sub{{font-size:11px;color:#666;margin-bottom:6px}}
.info-panel .legend{{display:flex;flex-wrap:wrap;gap:6px}}
.info-panel .legend span{{display:flex;align-items:center;gap:4px;font-size:11px;font-weight:600;font-family:monospace}}
.info-panel .legend .dot{{width:12px;height:12px;border-radius:3px;border:2px solid rgba(0,0,0,.3)}}
.layer-ctrl{{position:absolute;bottom:30px;right:12px;z-index:1000;background:rgba(255,255,255,0.95);padding:10px 14px;border-radius:10px;box-shadow:0 4px 20px rgba(0,0,0,.3);font-size:12px}}
.layer-ctrl label{{display:flex;align-items:center;gap:6px;padding:3px 0;cursor:pointer;font-weight:600}}
.parcel-label{{background:rgba(255,255,255,0.92);border:2px solid;padding:3px 10px;border-radius:6px;font-size:14px;font-weight:800;font-family:monospace;white-space:nowrap;box-shadow:0 2px 8px rgba(0,0,0,.4)}}
</style>
</head><body>
<div class="info-panel">
  <h3>Mapa dzialek</h3>
  <div class="sub">{title}</div>
  <div class="legend" id="legend"></div>
</div>
<div id="map"></div>
<div class="layer-ctrl">
  <div style="font-size:10px;color:#888;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;font-weight:700">Warstwy</div>
  <label><input type="checkbox" id="chkSat" checked onchange="toggleSat()"/> Satelita</label>
  <label><input type="checkbox" id="chkDzialki" checked onchange="toggleDz()"/> Granice dzialek</label>
  <label><input type="checkbox" id="chkNumery" checked onchange="toggleNr()"/> Numery dzialek</label>
  <label><input type="checkbox" id="chkOSM" onchange="toggleOSM()"/> Mapa drogowa</label>
</div>
<script>
var polygons={polygons_js};
var colors={str(colors)};
var map=L.map('map',{{zoomControl:true}}).setView([{center_lat},{center_lng}],16);
var satLayer=L.tileLayer('https://mt1.google.com/vt/lyrs=s&x={{x}}&y={{y}}&z={{z}}',{{maxZoom:21,attribution:'Google Satellite'}});
satLayer.addTo(map);
var osmLayer=L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',{{maxZoom:20,attribution:'OSM'}});
var dzLayer=L.tileLayer.wms('https://integracja.gugik.gov.pl/cgi-bin/KraijObiektServletNew',{{layers:'dzialki',format:'image/png',transparent:true,maxZoom:21,attribution:'EGiB',opacity:0.85}});
dzLayer.addTo(map);
var nrLayer=L.tileLayer.wms('https://integracja.gugik.gov.pl/cgi-bin/KraijObiektServletNew',{{layers:'numery_dzialek',format:'image/png',transparent:true,maxZoom:21,attribution:'EGiB'}});
nrLayer.addTo(map);
function toggleSat(){{if(document.getElementById('chkSat').checked)map.addLayer(satLayer);else map.removeLayer(satLayer)}}
function toggleDz(){{if(document.getElementById('chkDzialki').checked)map.addLayer(dzLayer);else map.removeLayer(dzLayer)}}
function toggleNr(){{if(document.getElementById('chkNumery').checked)map.addLayer(nrLayer);else map.removeLayer(nrLayer)}}
function toggleOSM(){{if(document.getElementById('chkOSM').checked)map.addLayer(osmLayer);else map.removeLayer(osmLayer)}}
var bounds=L.latLngBounds();
var legend=document.getElementById('legend');
polygons.forEach(function(p,i){{
  if(p.coords.length<3) return;
  var c=colors[i%colors.length];
  var poly=L.polygon(p.coords,{{color:c,weight:4,fillColor:c,fillOpacity:0.25}}).addTo(map);
  var lats=p.coords.map(function(x){{return x[0]}});
  var lngs=p.coords.map(function(x){{return x[1]}});
  var cLat=(Math.min.apply(null,lats)+Math.max.apply(null,lats))/2;
  var cLng=(Math.min.apply(null,lngs)+Math.max.apply(null,lngs))/2;
  var label=L.divIcon({{className:'',html:'<div class="parcel-label" style="border-color:'+c+';color:'+c+'">'+p.nr+'</div>',iconSize:[null,null],iconAnchor:[30,14]}});
  L.marker([cLat,cLng],{{icon:label,interactive:false}}).addTo(map);
  poly.bindPopup('<div style="font-family:monospace;text-align:center"><b style="font-size:16px;color:'+c+'">'+p.nr+'</b><br><span style="font-size:11px;color:#666">'+p.teryt+'</span></div>');
  bounds.extend(poly.getBounds());
  legend.innerHTML+='<span><span class="dot" style="background:'+c+'"></span>'+p.nr+'</span>';
}});
if(bounds.isValid()) map.fitBounds(bounds.pad(0.15));
L.control.scale({{imperial:false,position:'bottomleft'}}).addTo(map);
</script>
</body></html>"""
    return HTMLResponse(html)


@app.get("/")
async def root():
    index = os.path.join(static_dir, "index.html")
    if os.path.exists(index):
        return FileResponse(index)
    return JSONResponse({"status": "Kabanek Gospodarstwo CRM API", "docs": "/docs"})


@app.get("/manifest.json")
async def manifest():
    return FileResponse(os.path.join(static_dir, "manifest.json"), media_type="application/manifest+json")


@app.get("/sw.js")
async def service_worker():
    return FileResponse(os.path.join(static_dir, "sw.js"), media_type="application/javascript",
                        headers={"Service-Worker-Allowed": "/"})


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
