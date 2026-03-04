from .auth_routes import router as auth_router
from .tuczarnie_routes import router as tuczarnie_router
from .roslinna_routes import router as roslinna_router
from .admin_routes import router as admin_router
from .files_routes import router as files_router
from .bioasekuracja_routes import router as bioasekuracja_router

def register_routes(app):
    app.include_router(auth_router)
    app.include_router(tuczarnie_router)
    app.include_router(roslinna_router)
    app.include_router(admin_router)
    app.include_router(files_router)
    app.include_router(bioasekuracja_router)
