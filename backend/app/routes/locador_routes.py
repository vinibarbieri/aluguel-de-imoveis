"""
Módulo de rotas do locador.
Este arquivo contém as rotas relacionadas às operações que um locador pode realizar:
- Gerenciamento de imóveis (criar, listar, atualizar, deletar)
- Gerenciamento de reservas (visualizar, aprovar/recusar)
"""

from flask import Blueprint, request, jsonify
from app.data_manager import save_data, find_many, find_by_id, delete_data
from datetime import datetime

# Cria um blueprint para agrupar as rotas do locador
locador_bp = Blueprint('locador', __name__)

@locador_bp.route("/properties", methods=["POST"])
def create_property():
    """
    Rota para criar um novo imóvel.
    
    Recebe:
    - title: Título do imóvel
    - description: Descrição do imóvel
    - address: Endereço do imóvel
    - city: Cidade do imóvel (opcional)
    - price_per_day: Preço por dia
    - available_from: Data de disponibilidade inicial
    - available_until: Data de disponibilidade final
    - owner_id: ID do proprietário
    - image_url: URL da imagem do imóvel (opcional)
    
    Retorna:
    - 201: Imóvel cadastrado com sucesso
    """
    data = request.get_json()
    property_data = {
        "title": data["title"],
        "description": data["description"],
        "address": data["address"],
        "city": data.get("city", ""),
        "price_per_day": data["price_per_day"],
        "available_from": data["available_from"],
        "available_until": data["available_until"],
        "owner_id": data["owner_id"],
        "image_url": data.get("image_url")
    }
    
    saved_property = save_data('properties', property_data)
    return jsonify({"message": "Imóvel cadastrado", "property_id": saved_property['id']}), 201

@locador_bp.route("/properties/<owner_id>", methods=["GET"])
def get_properties(owner_id):
    """
    Rota para listar todos os imóveis de um locador.
    Inclui avaliação média e número de reservas para cada imóvel.
    
    Recebe:
    - owner_id: ID do proprietário
    
    Retorna:
    - Lista de imóveis com informações detalhadas
    """
    properties = find_many('properties', {'owner_id': owner_id})
    result = []
    
    for p in properties:
        # Busca todas as reservas deste imóvel
        reservations = find_many('reservations', {'property_id': p['id']})
        
        # Busca todas as avaliações deste imóvel
        reviews = [r for r in find_many('reviews') if r['reservation_id'] in [res['id'] for res in reservations]]
        
        avg_rating = round(sum(r['rating'] for r in reviews) / len(reviews), 1) if reviews else None
        
        result.append({
            "id": p['id'],
            "title": p['title'],
            "description": p['description'],
            "address": p['address'],
            "price_per_day": p['price_per_day'],
            "available_from": p['available_from'],
            "available_until": p['available_until'],
            "image_url": p.get('image_url'),
            "average_rating": avg_rating,
            "total_reservas": len(reservations)
        })
    
    return jsonify(result)

@locador_bp.route("/property/<id>", methods=["PUT"])
def update_property(id):
    """
    Rota para atualizar informações de um imóvel.
    
    Recebe:
    - id: ID do imóvel
    - title: Novo título
    - description: Nova descrição
    - address: Novo endereço
    - price_per_day: Novo preço por dia
    - available_from: Nova data de disponibilidade inicial
    - available_until: Nova data de disponibilidade final
    - image_url: Nova URL da imagem (opcional)
    
    Retorna:
    - 200: Imóvel atualizado com sucesso
    - 404: Imóvel não encontrado
    """
    data = request.get_json()
    property_data = find_by_id('properties', id)
    
    if not property_data:
        return jsonify({"error": "Imóvel não encontrado"}), 404
    
    property_data.update({
        "title": data["title"],
        "description": data["description"],
        "address": data["address"],
        "price_per_day": data["price_per_day"],
        "available_from": data["available_from"],
        "available_until": data["available_until"],
        "image_url": data.get("image_url")
    })
    
    save_data('properties', property_data)
    return jsonify({"message": "Imóvel atualizado"})

@locador_bp.route("/property/<id>", methods=["DELETE"])
def delete_property(id):
    """
    Rota para deletar um imóvel.
    
    Recebe:
    - id: ID do imóvel
    
    Retorna:
    - 200: Imóvel removido com sucesso
    - 404: Imóvel não encontrado
    """
    if delete_data('properties', id):
        return jsonify({"message": "Imóvel removido"})
    return jsonify({"error": "Imóvel não encontrado"}), 404

@locador_bp.route("/reservations/<owner_id>", methods=["GET"])
def get_reservations(owner_id):
    """
    Rota para listar todas as reservas recebidas para os imóveis do locador.
    
    Recebe:
    - owner_id: ID do proprietário
    
    Retorna:
    - Lista de reservas com informações do locatário
    """
    # Busca todos os imóveis deste proprietário
    properties = find_many('properties', {'owner_id': owner_id})
    property_ids = [p['id'] for p in properties]
    
    # Busca todas as reservas para estes imóveis
    all_reservations = find_many('reservations')
    reservations = [r for r in all_reservations if r['property_id'] in property_ids]
    
    result = []
    for r in reservations:
        # Busca informações do locatário
        renter = find_by_id('users', r['renter_id'])
        result.append({
            "reservation_id": r['id'],
            "property_id": r['property_id'],
            "renter_name": renter['name'] if renter else "Unknown",
            "start_date": r['start_date'],
            "end_date": r['end_date'],
            "approved": r.get('approved', False)
        })
    
    return jsonify(result)

@locador_bp.route("/reservation/<id>", methods=["PUT"])
def update_reservation(id):
    """
    Rota para aprovar ou recusar uma reserva.
    
    Recebe:
    - id: ID da reserva
    - approved: Boolean indicando se a reserva foi aprovada
    
    Retorna:
    - 200: Reserva atualizada com sucesso
    - 404: Reserva não encontrada
    """
    data = request.get_json()
    reservation = find_by_id('reservations', id)
    
    if not reservation:
        return jsonify({"error": "Reserva não encontrada"}), 404
    
    reservation['approved'] = data["approved"]
    save_data('reservations', reservation)
    return jsonify({"message": "Reserva atualizada"})
