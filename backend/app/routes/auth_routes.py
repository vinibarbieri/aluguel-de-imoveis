"""
Módulo de rotas de autenticação.
Este arquivo contém as rotas relacionadas à autenticação de usuários:
- Registro de novos usuários
- Login de usuários existentes
- Edição de informações do usuário
"""

from flask import Blueprint, request, jsonify
from app.data_manager import save_data, find_many
from app.services.auth_service import update_user_info

# Cria um blueprint para agrupar as rotas de autenticação
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Rota para registro de novos usuários.
    
    Recebe:
    - name: Nome do usuário
    - email: Email do usuário
    - user_type: Tipo do usuário (locador ou locatario)
    
    Retorna:
    - 201: Usuário cadastrado com sucesso
    - 400: Dados inválidos
    - 409: Email já cadastrado
    """
    data = request.json
    name = data.get('name')
    email = data.get('email')
    user_type = data.get('user_type')  # locador ou locatario

    if not name or not email or user_type not in ['locador', 'locatario']:
        return jsonify({'error': 'Dados inválidos'}), 400

    # Verifica se o email já está cadastrado
    existing_users = find_many('users', {'email': email})
    if existing_users:
        return jsonify({'error': 'E-mail já cadastrado'}), 409

    user = {
        'name': name,
        'email': email,
        'user_type': user_type
    }
    
    saved_user = save_data('users', user)

    return jsonify({
        'message': 'Usuário cadastrado com sucesso',
        'user_id': saved_user['id']
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Rota para login de usuários.
    
    Recebe:
    - email: Email do usuário
    
    Retorna:
    - 200: Login bem-sucedido com informações do usuário
    - 400: Email não fornecido
    - 404: Usuário não encontrado
    """
    data = request.json
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email é obrigatório'}), 400

    users = find_many('users', {'email': email})
    if not users:
        return jsonify({'error': 'Usuário não encontrado'}), 404

    user = users[0]  # Get the first matching user
    return jsonify({
        'message': 'Login bem-sucedido',
        'user': {
            'id': user['id'],
            'name': user['name'],
            'email': user['email'],
            'user_type': user['user_type']
        }
    }), 200

@auth_bp.route("/edit", methods=["PUT"])
def edit_user():
    """
    Rota para edição de informações do usuário.
    
    Recebe:
    - id: ID do usuário
    - name: Novo nome do usuário
    - email: Novo email do usuário
    
    Retorna:
    - 200: Dados atualizados com sucesso
    - 400: Erro na atualização
    """
    data = request.json
    user_id = data.get("id")  # ou você pode pegar de um token se estiver usando autenticação
    name = data.get("name")
    email = data.get("email")

    try:
        update_user_info(user_id, name, email)
        return jsonify({"message": "Dados atualizados com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
