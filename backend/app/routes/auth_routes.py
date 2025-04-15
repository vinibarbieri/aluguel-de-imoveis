# backend/routes/auth_routes.py

from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    user_type = data.get('user_type')  # locador ou locatario

    if not name or not email or user_type not in ['locador', 'locatario']:
        return jsonify({'error': 'Dados inválidos'}), 400

    # Verifica se o email já está cadastrado
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'E-mail já cadastrado'}), 409

    user = User(name=name, email=email, user_type=user_type)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Usuário cadastrado com sucesso', 'user_id': user.id}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email é obrigatório'}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404

    return jsonify({
        'message': 'Login bem-sucedido',
        'user': {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'user_type': user.user_type
        }
    }), 200
