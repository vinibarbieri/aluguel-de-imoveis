"""
Módulo de rotas do locatário.
Este arquivo contém as rotas relacionadas às operações que um locatário pode realizar:
- Busca de imóveis disponíveis
- Realização de reservas
- Gerenciamento de reservas próprias
- Criação e visualização de avaliações
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, date
from app.data_manager import find_many, find_by_id, save_data
import uuid
import unicodedata

# Cria um blueprint para agrupar as rotas do locatário
locatario_bp = Blueprint('locatario', __name__)

def parse_date(date_str):
    """
    Converte uma string de data no formato YYYY-MM-DD para um objeto date.
    
    Args:
        date_str: String contendo a data no formato YYYY-MM-DD
        
    Returns:
        date: Objeto date correspondente à string
    """
    return datetime.strptime(date_str, "%Y-%m-%d").date()

def is_overlapping(start1, end1, start2, end2):
    """
    Verifica se dois intervalos de datas se sobrepõem.
    
    Args:
        start1: Data inicial do primeiro intervalo
        end1: Data final do primeiro intervalo
        start2: Data inicial do segundo intervalo
        end2: Data final do segundo intervalo
        
    Returns:
        bool: True se os intervalos se sobrepõem, False caso contrário
    """
    return start1 <= end2 and start2 <= end1

def normalize(text):
    """
    Normaliza um texto removendo acentos e convertendo para minúsculas.
    
    Args:
        text: Texto a ser normalizado
        
    Returns:
        str: Texto normalizado
    """
    if not text:
        return ""
    return unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode("utf-8").lower()

@locatario_bp.route('/search', methods=['GET'])
def search_properties():
    """
    Rota para buscar imóveis disponíveis com filtros.
    
    Parâmetros de busca:
    - city: Cidade do imóvel
    - min_price: Preço mínimo por dia
    - max_price: Preço máximo por dia
    - start_date: Data inicial da estadia
    - end_date: Data final da estadia
    
    Retorna:
    - Lista de imóveis disponíveis que atendem aos critérios de busca
    """
    city = request.args.get('city', "")
    min_price = float(request.args.get('min_price', 0))
    max_price = float(request.args.get('max_price', 1e9))
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    properties = find_many('properties')
    result = []

    for p in properties:
        # Filtro por preço
        if not (min_price <= p["price_per_day"] <= max_price):
            continue
        
        # Filtro por cidade (normalizado)
        if city:
            normalized_city = normalize(city)
            property_city = normalize(p.get("city", ""))
            property_address = normalize(p.get("address", ""))

            if normalized_city not in property_city and normalized_city not in property_address:
                continue

        # Verificar disponibilidade
        if start_date and end_date:
            start = parse_date(start_date)
            end = parse_date(end_date)

            if start < parse_date(p["available_from"]) or end > parse_date(p["available_until"]):
                continue

            reservations = find_many('reservations', {"property_id": p["id"]})
            for r in reservations:
                if r.get("approved"):
                    if is_overlapping(start, end, parse_date(r["start_date"]), parse_date(r["end_date"])):
                        break
            else:
                pass  # disponível

        # calcular média de avaliações
        reservations = find_many('reservations', {"property_id": p["id"]})
        reviews = [rv for r in reservations for rv in find_many('reviews', {"reservation_id": r["id"]})]
        avg_rating = round(sum(r["rating"] for r in reviews) / len(reviews), 1) if reviews else None

        result.append({
            "id": p["id"],
            "title": p["title"],
            "description": p["description"],
            "address": p["address"],
            "price_per_day": p["price_per_day"],
            "available_from": p["available_from"],
            "available_until": p["available_until"],
            "image_url": p.get("image_url"),
            "average_rating": avg_rating
        })

    return jsonify(result)

@locatario_bp.route('/reserve', methods=['POST'])
def reserve_property():
    """
    Rota para realizar uma reserva de imóvel.
    
    Recebe:
    - property_id: ID do imóvel
    - renter_id: ID do locatário
    - start_date: Data inicial da reserva
    - end_date: Data final da reserva
    
    Retorna:
    - 201: Reserva solicitada com sucesso
    - 400: Dados inválidos ou datas fora do período disponível
    - 409: Já existe uma reserva no período solicitado
    """
    data = request.get_json()
    property_id = data.get("property_id")
    renter_id = data.get("renter_id")
    start_date = parse_date(data.get("start_date"))
    end_date = parse_date(data.get("end_date"))

    prop = find_by_id("properties", property_id)
    renter = find_by_id("users", renter_id)

    if not prop or not renter or renter["user_type"] != "locatario":
        return jsonify({"error": "Dados inválidos"}), 400

    if start_date < parse_date(prop["available_from"]) or end_date > parse_date(prop["available_until"]):
        return jsonify({"error": "Datas fora do período disponível"}), 400

    existing = find_many("reservations", {"property_id": prop["id"]})
    for r in existing:
        if r.get("approved") and is_overlapping(start_date, end_date, parse_date(r["start_date"]), parse_date(r["end_date"])):
            return jsonify({"error": "Já existe uma reserva nesse período"}), 409

    reservation = {
        "id": str(uuid.uuid4()),
        "property_id": property_id,
        "renter_id": renter_id,
        "start_date": data.get("start_date"),
        "end_date": data.get("end_date"),
        "approved": None
    }
    save_data("reservations", reservation)
    return jsonify({"message": "Reserva solicitada com sucesso", "reservation_id": reservation["id"]}), 201

@locatario_bp.route('/my-reservations/<user_id>', methods=['GET'])
def list_my_reservations(user_id):
    """
    Rota para listar as reservas de um locatário.
    
    Recebe:
    - user_id: ID do locatário
    
    Retorna:
    - Lista de reservas com informações do imóvel e avaliações
    - 403: Usuário inválido
    """
    user = find_by_id("users", user_id)
    if not user or user["user_type"] != "locatario":
        return jsonify({"error": "Usuário inválido"}), 403

    reservations = find_many("reservations", {"renter_id": user_id})
    result = []

    for r in reservations:
        prop = find_by_id("properties", r["property_id"])
        review = find_many("reviews", {"reservation_id": r["id"]})
        result.append({
            "reservation_id": r["id"],
            "property_id": r["property_id"],
            "property_title": prop["title"] if prop else "Desconhecido",
            "start_date": r["start_date"],
            "end_date": r["end_date"],
            "approved": r.get("approved"),
            "image_url": prop.get("image_url") if prop else None,
            "review": review[0] if review else None
        })

    return jsonify(result)

@locatario_bp.route('/review', methods=['POST'])
def create_review():
    """
    Rota para criar uma avaliação de um imóvel.
    
    Recebe:
    - reservation_id: ID da reserva
    - rating: Nota da avaliação (1-5)
    - comment: Comentário da avaliação
    
    Retorna:
    - 201: Avaliação registrada com sucesso
    - 400: Nota inválida, reserva já avaliada ou reserva ainda não finalizada
    - 404: Reserva não encontrada
    """
    data = request.get_json()
    reservation_id = data.get("reservation_id")
    rating = data.get("rating")
    comment = data.get("comment")

    if not (1 <= rating <= 5):
        return jsonify({"error": "Nota deve ser entre 1 e 5"}), 400

    reservation = find_by_id("reservations", reservation_id)
    if not reservation:
        return jsonify({"error": "Reserva não encontrada"}), 404

    existing_review = find_many("reviews", {"reservation_id": reservation_id})
    if existing_review:
        return jsonify({"error": "Reserva já foi avaliada"}), 400

    if parse_date(reservation["end_date"]) > date.today():
        return jsonify({"error": "Só é possível avaliar após o fim da reserva"}), 400

    review = {
        "id": str(uuid.uuid4()),
        "reservation_id": reservation_id,
        "rating": rating,
        "comment": comment
    }
    save_data("reviews", review)
    return jsonify({"message": "Avaliação registrada com sucesso"}), 201

@locatario_bp.route('/property/<property_id>/reviews', methods=['GET'])
def list_reviews(property_id):
    """
    Rota para listar as avaliações de um imóvel.
    
    Recebe:
    - property_id: ID do imóvel
    
    Retorna:
    - Lista de avaliações com informações do locatário
    """
    reservations = find_many("reservations", {"property_id": property_id})
    result = []

    for r in reservations:
        review = find_many("reviews", {"reservation_id": r["id"]})
        if review:
            renter = find_by_id("users", r["renter_id"])
            result.append({
                "rating": review[0]["rating"],
                "comment": review[0]["comment"],
                "renter_name": renter["name"] if renter else "Anônimo"
            })

    return jsonify(result)
