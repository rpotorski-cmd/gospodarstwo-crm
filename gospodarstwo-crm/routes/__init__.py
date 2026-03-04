from .auth_routes import auth_bp
from .tuczarnie_routes import tuczarnie_bp
from .roslinna_routes import roslinna_bp
from .admin_routes import admin_bp
from .files_routes import files_bp
from .bioasekuracja_routes import bioasekuracja_bp

def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(tuczarnie_bp)
    app.register_blueprint(roslinna_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(files_bp)
    app.register_blueprint(bioasekuracja_bp)
