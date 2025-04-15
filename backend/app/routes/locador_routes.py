# app/routes/locador_routes.py

from flask import Blueprint, request, jsonify
from app.models.property import Property
from app.models.reservation import Reservation
from app.models.review import Review
from app import db
from datetime import datetime

locador_bp = Blueprint('locador', __name__)

# Criar imóvel
@locador_bp.route("/properties", methods=["POST"])
def create_property():
    data = request.get_json()
    property = Property(
        title=data["title"],
        description=data["description"],
        address=data["address"],
        price_per_day=data["price_per_day"],
        available_from=datetime.strptime(data["available_from"], "%Y-%m-%d").date(),
        available_until=datetime.strptime(data["available_until"], "%Y-%m-%d").date(),
        owner_id=data["owner_id"],
        image_url=data.get("image_url")  # Novo campo
    )
    db.session.add(property)
    db.session.commit()
    return jsonify({"message": "Imóvel cadastrado"}), 201

# Listar imóveis do locador com avaliação média e nº de reservas
@locador_bp.route("/properties/<int:owner_id>", methods=["GET"])
def get_properties(owner_id):
    properties = Property.query.filter_by(owner_id=owner_id).all()
    result = []
    for p in properties:
        reviews = [r.review for r in p.reservations if r.review]
        avg_rating = round(sum(rv.rating for rv in reviews) / len(reviews), 1) if reviews else None
        result.append({
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "address": p.address,
            "price_per_day": p.price_per_day,
            "available_from": p.available_from.isoformat(),
            "available_until": p.available_until.isoformat(),
            "image_url": p.image_url,
            "average_rating": avg_rating,
            "total_reservas": len(p.reservations)
        })
    return jsonify(result)

# Atualizar imóvel
@locador_bp.route("/property/<int:id>", methods=["PUT"])
def update_property(id):
    data = request.get_json()
    p = Property.query.get_or_404(id)
    p.title = data["title"]
    p.description = data["description"]
    p.address = data["address"]
    p.price_per_day = data["price_per_day"]
    p.available_from = datetime.strptime(data["available_from"], "%Y-%m-%d").date()
    p.available_until = datetime.strptime(data["available_until"], "%Y-%m-%d").date()
    p.image_url = data.get("image_url")
    db.session.commit()
    return jsonify({"message": "Imóvel atualizado"})

# Deletar imóvel
@locador_bp.route("/property/<int:id>", methods=["DELETE"])
def delete_property(id):
    p = Property.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return jsonify({"message": "Imóvel removido"})

# Reservas recebidas
@locador_bp.route("/reservations/<int:owner_id>", methods=["GET"])
def get_reservations(owner_id):
    reservations = Reservation.query.join(Property).filter(Property.owner_id == owner_id).all()
    result = []
    for r in reservations:
        result.append({
            "reservation_id": r.id,
            "property_id": r.property_id,
            "renter_name": r.renter.name,
            "start_date": r.start_date.isoformat(),
            "end_date": r.end_date.isoformat(),
            "approved": r.approved
        })
    return jsonify(result)

# Aprovar ou recusar reserva
@locador_bp.route("/reservation/<int:id>", methods=["PUT"])
def update_reservation(id):
    data = request.get_json()
    r = Reservation.query.get_or_404(id)
    r.approved = data["approved"]
    db.session.commit()
    return jsonify({"message": "Reserva atualizada"})
