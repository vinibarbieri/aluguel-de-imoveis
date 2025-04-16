"""
Módulo principal da aplicação Flask.
Este arquivo configura e inicializa a aplicação web, incluindo:
- Configuração do Flask
- Habilitação do CORS
- Registro de blueprints para diferentes rotas da API
"""

from flask import Flask
from flask_cors import CORS
import os

def create_app():
    """
    Função factory que cria e configura a aplicação Flask.
    
    Returns:
        Flask: A aplicação Flask configurada com todos os blueprints e configurações necessárias
    """
    app = Flask(__name__)
    
    # Habilita CORS (Cross-Origin Resource Sharing) para permitir requisições
    # do frontend em diferentes domínios
    CORS(app)

    # Garante que a pasta de dados exista para armazenamento de arquivos
    # como imagens de imóveis e documentos
    os.makedirs("data", exist_ok=True)

    # Registra os blueprints das rotas da API
    # Cada blueprint contém um conjunto específico de rotas relacionadas
    from routes.auth_routes import auth_bp  # Rotas de autenticação
    from routes.locador_routes import locador_bp  # Rotas do locador
    from routes.locatario_routes import locatario_bp  # Rotas do locatário

    # Registra cada blueprint com seu respectivo prefixo de URL
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(locador_bp, url_prefix='/api/locador')
    app.register_blueprint(locatario_bp, url_prefix='/api/locatario')

    return app
