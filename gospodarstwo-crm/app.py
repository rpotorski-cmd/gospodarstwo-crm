from flask import Flask
from flask_cors import CORS
import os
from database import init_db
from routes import register_routes

app = Flask(__name__)

# ✅ CORS FIX - Pozwala na requesty z GitHub Pages!
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Konfiguracja
app.config['DATABASE_URL'] = os.environ.get('DATABASE_URL')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Inicjalizacja bazy danych
init_db(app)

# Rejestracja routes
register_routes(app)

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health():
    return {
        'success': True,
        'status': 'OK',
        'database': 'connected'
    }

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
