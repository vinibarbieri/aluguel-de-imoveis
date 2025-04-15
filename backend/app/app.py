# backend/app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Inicializa o SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configurações do banco de dados SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rental.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Habilita CORS (para conectar com o frontend React)
    CORS(app)

    # Inicializa o banco com a app
    db.init_app(app)

    # Importa e registra os blueprints de rotas
    from routes.auth_routes import auth_bp
    from routes.locador_routes import locador_bp
    from routes.locatario_routes import locatario_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(locador_bp, url_prefix='/api/locador')
    app.register_blueprint(locatario_bp, url_prefix='/api/locatario')

    return app
