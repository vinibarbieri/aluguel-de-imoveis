# backend/app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rental.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    CORS(app)
    db.init_app(app)

    # Importa e registra as rotas
    from app.routes.auth_routes import auth_bp
    from app.routes.locador_routes import locador_bp
    from app.routes.locatario_routes import locatario_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(locador_bp, url_prefix='/api/locador')
    app.register_blueprint(locatario_bp, url_prefix='/api/locatario')

    return app
