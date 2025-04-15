# backend/routes/locador_routes.py

from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models.property import Property
from app.models.reservation import Reservation
from app.models.user import User

locador_bp = Blueprint('locador', __name__)

def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").date()

@locador_bp.route('/properties', methods=['POST'])
def create_property():
    data = request.json
    owner_id = data.get('owner_id')

    owner = User.query.get(owner_id)
    if not owner or owner.user_type != 'locador':
        return jsonify({'error': 'Usuário inválido'}), 403

    property = Property(
        title=data['title'],
        description=data['description'],
        address=data['address'],
        price_per_day=data['price_per_day'],
        available_from=parse_date(data['available_from']),
        available_until=parse_date(data['available_until']),
        owner_id=owner_id
    )

    db.session.add(property)
    db.session.commit()

    return jsonify({'message': 'Imóvel cadastrado com sucesso', 'property_id': property.id}), 201


@locador_bp.route('/properties/<int:owner_id>', methods=['GET'])
def list_properties(owner_id):
    properties = Property.query.filter_by(owner_id=owner_id).all()
    return jsonify([{
        'id': p.id,
        'title': p.title,
        'price_per_day': p.price_per_day,
        'available_from': p.available_from.isoformat(),
        'available_until': p.available_until.isoformat()
    } for p in properties])


@locador_bp.route('/property/<int:property_id>', methods=['PUT'])
def edit_property(property_id):
    data = request.json
    property = Property.query.get(property_id)

    if not property:
        return jsonify({'error': 'Imóvel não encontrado'}), 404

    property.title = data.get('title', property.title)
    property.description = data.get('description', property.description)
    property.address = data.get('address', property.address)
    property.price_per_day = data.get('price_per_day', property.price_per_day)

    if 'available_from' in data:
        property.available_from = parse_date(data['available_from'])
    if 'available_until' in data:
        property.available_until = parse_date(data['available_until'])

    db.session.commit()
    return jsonify({'message': 'Imóvel atualizado com sucesso'})


@locador_bp.route('/reservations/<int:owner_id>', methods=['GET'])
def list_reservations(owner_id):
    properties = Property.query.filter_by(owner_id=owner_id).all()
    property_ids = [p.id for p in properties]

    reservations = Reservation.query.filter(Reservation.property_id.in_(property_ids)).all()

    return jsonify([{
        'reservation_id': r.id,
        'property_id': r.property_id,
        'renter_name': r.renter.name,
        'start_date': r.start_date.isoformat(),
        'end_date': r.end_date.isoformat(),
        'approved': r.approved
    } for r in reservations])


@locador_bp.route('/reservation/<int:reservation_id>', methods=['PUT'])
def update_reservation_status(reservation_id):
    data = request.json
    approved = data.get('approved')  # True ou False

    reservation = Reservation.query.get(reservation_id)
    if reservation is None:
        return jsonify({'error': 'Reserva não encontrada'}), 404

    reservation.approved = approved
    db.session.commit()

    return jsonify({'message': 'Status da reserva atualizado'})


@locador_bp.route('/reviews/<int:owner_id>', methods=['GET'])
def get_reviews_by_owner(owner_id):
    from models.review import Review  # importar aqui para evitar ciclos

    # Pega todos os imóveis do locador
    properties = Property.query.filter_by(owner_id=owner_id).all()
    property_ids = [p.id for p in properties]

    # Pega todas as reservas desses imóveis que têm review
    reservations = Reservation.query.filter(Reservation.property_id.in_(property_ids)).all()
    reviews = [r.review for r in reservations if r.review]

    return jsonify([{
        'property_id': rv.reservation.property.id,
        'property_title': rv.reservation.property.title,
        'renter_name': rv.reservation.renter.name,
        'rating': rv.rating,
        'comment': rv.comment
    } for rv in reviews])
