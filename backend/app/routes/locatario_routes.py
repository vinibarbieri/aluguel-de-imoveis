# backend/routes/locatario_routes.py

from flask import Blueprint, request, jsonify
from datetime import datetime, date
from app import db
from app.models.property import Property
from app.models.reservation import Reservation
from app.models.user import User
from app.models.review import Review

locatario_bp = Blueprint('locatario', __name__)

def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").date()

def is_overlapping(start1, end1, start2, end2):
    return start1 <= end2 and start2 <= end1

@locatario_bp.route('/search', methods=['GET'])
def search_properties():
    city = request.args.get('city')  # parte do address
    min_price = float(request.args.get('min_price', 0))
    max_price = float(request.args.get('max_price', 1e9))
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = Property.query.filter(
        Property.price_per_day >= min_price,
        Property.price_per_day <= max_price
    )

    if city:
        query = query.filter(Property.address.ilike(f"%{city}%"))

    properties = query.all()

    result = []

    for p in properties:
        # Verifica disponibilidade
        if start_date and end_date:
            start = parse_date(start_date)
            end = parse_date(end_date)

            if start < p.available_from or end > p.available_until:
                continue

            conflict = False
            for r in p.reservations:
                if r.approved and is_overlapping(start, end, r.start_date, r.end_date):
                    conflict = True
                    break
            if conflict:
                continue

        # Calcula a média de avaliações
        reviews = [r.review for r in p.reservations if r.review]
        avg_rating = (
            round(sum(rv.rating for rv in reviews) / len(reviews), 1)
            if reviews else None
        )

        result.append({
            'id': p.id,
            'title': p.title,
            'description': p.description,
            'address': p.address,
            'price_per_day': p.price_per_day,
            'available_from': p.available_from.isoformat(),
            'available_until': p.available_until.isoformat(),
            'average_rating': avg_rating
        })

    return jsonify(result)



# 2. Reservar um imóvel
@locatario_bp.route('/reserve', methods=['POST'])
def reserve_property():
    data = request.json
    property_id = data.get('property_id')
    renter_id = data.get('renter_id')
    start_date = parse_date(data.get('start_date'))
    end_date = parse_date(data.get('end_date'))

    property = Property.query.get(property_id)
    renter = User.query.get(renter_id)

    if not property or not renter or renter.user_type != 'locatario':
        return jsonify({'error': 'Dados inválidos'}), 400

    # Verifica se as datas estão dentro da disponibilidade
    if start_date < property.available_from or end_date > property.available_until:
        return jsonify({'error': 'Datas fora do período disponível'}), 400

    # Verifica sobreposição com reservas aprovadas
    for r in property.reservations:
        if r.approved and is_overlapping(start_date, end_date, r.start_date, r.end_date):
            return jsonify({'error': 'Já existe uma reserva nesse período'}), 409

    reservation = Reservation(
        property_id=property_id,
        renter_id=renter_id,
        start_date=start_date,
        end_date=end_date,
        approved=None  # pendente
    )

    db.session.add(reservation)
    db.session.commit()

    return jsonify({'message': 'Reserva solicitada com sucesso', 'reservation_id': reservation.id}), 201


# 3. Ver minhas reservas
@locatario_bp.route('/my-reservations/<int:user_id>', methods=['GET'])
def list_my_reservations(user_id):
    user = User.query.get(user_id)

    if not user or user.user_type != 'locatario':
        return jsonify({'error': 'Usuário inválido'}), 403

    reservations = Reservation.query.filter_by(renter_id=user_id).all()

    return jsonify([{
        'reservation_id': r.id,
        'property_id': r.property_id,
        'property_title': r.property.title,
        'start_date': r.start_date.isoformat(),
        'end_date': r.end_date.isoformat(),
        'approved': r.approved
    } for r in reservations])


@locatario_bp.route('/review', methods=['POST'])
def create_review():
    data = request.json
    reservation_id = data.get('reservation_id')
    rating = data.get('rating')
    comment = data.get('comment')

    if not (1 <= rating <= 5):
        return jsonify({'error': 'Nota deve ser entre 1 e 5'}), 400

    reservation = Reservation.query.get(reservation_id)
    if not reservation:
        return jsonify({'error': 'Reserva não encontrada'}), 404

    if reservation.review:
        return jsonify({'error': 'Reserva já foi avaliada'}), 400

    if reservation.end_date > date.today():
        return jsonify({'error': 'Só é possível avaliar após o fim da reserva'}), 400

    review = Review(
        reservation_id=reservation_id,
        rating=rating,
        comment=comment
    )

    db.session.add(review)
    db.session.commit()

    return jsonify({'message': 'Avaliação registrada com sucesso'}), 201


@locatario_bp.route('/property/<int:property_id>/reviews', methods=['GET'])
def list_reviews(property_id):
    reservations = Reservation.query.filter_by(property_id=property_id).all()
    reviews = [r.review for r in reservations if r.review]

    return jsonify([{
        'rating': rv.rating,
        'comment': rv.comment,
        'renter_name': rv.reservation.renter.name
    } for rv in reviews])
