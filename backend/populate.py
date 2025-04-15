from app import create_app, db
from app.models.user import User
from app.models.property import Property
from app.models.reservation import Reservation
from app.models.review import Review
from datetime import date, timedelta

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # USERS
    locador1 = User(name="Alice Locadora", email="alice@loca.com", user_type="locador")
    locador2 = User(name="Bruno Locador", email="bruno@loca.com", user_type="locador")

    locatario1 = User(name="Carlos Cliente", email="carlos@cli.com", user_type="locatario")
    locatario2 = User(name="Diana Cliente", email="diana@cli.com", user_type="locatario")

    db.session.add_all([locador1, locador2, locatario1, locatario2])
    db.session.commit()

    # PROPERTIES
    imovel1 = Property(
        title="Casa na Praia",
        description="Linda casa com vista para o mar.",
        address="Rua das Ondas, Florianópolis",
        price_per_day=300,
        available_from=date(2025, 4, 10),
        available_until=date(2025, 12, 31),
        owner_id=locador1.id,
        image_url="https://images.unsplash.com/photo-1505693416388-ac5ce068fe85"
    )

    imovel2 = Property(
        title="Apartamento Central",
        description="Perfeito para negócios.",
        address="Centro, São Paulo",
        price_per_day=200,
        available_from=date(2025, 3, 1),
        available_until=date(2025, 10, 15),
        owner_id=locador1.id,
        image_url="https://images.unsplash.com/photo-1600585154340-be6161a56a0c"
    )

    imovel3 = Property(
        title="Cabana na Serra",
        description="Ideal para descanso e natureza.",
        address="Serra do Rio do Rastro",
        price_per_day=180,
        available_from=date(2025, 5, 1),
        available_until=date(2025, 12, 31),
        owner_id=locador2.id,
        image_url="https://images.unsplash.com/photo-1570129477492-45c003edd2be"
    )

    imovel4 = Property(
        title="Flat moderno",
        description="Próximo ao aeroporto.",
        address="Bairro Aeroporto, Belo Horizonte",
        price_per_day=220,
        available_from=date(2025, 2, 1),
        available_until=date(2025, 11, 1),
        owner_id=locador2.id,
        image_url="https://images.unsplash.com/photo-1588854337221-4d6c71f5c111"
    )

    db.session.add_all([imovel1, imovel2, imovel3, imovel4])
    db.session.commit()

    # RESERVATIONS + REVIEWS
    def create_reservation_with_review(property, renter, days_ago, duration, rating, comment):
        start = date.today() - timedelta(days=days_ago)
        end = start + timedelta(days=duration)
        reservation = Reservation(
            property_id=property.id,
            renter_id=renter.id,
            start_date=start,
            end_date=end,
            approved=True
        )
        db.session.add(reservation)
        db.session.flush()  # necessário para criar ID antes do review
        review = Review(
            reservation_id=reservation.id,
            rating=rating,
            comment=comment
        )
        db.session.add(review)

    create_reservation_with_review(imovel1, locatario1, 30, 5, 5, "Maravilhosa estadia!")
    create_reservation_with_review(imovel2, locatario2, 45, 3, 4, "Boa localização e limpo.")
    create_reservation_with_review(imovel3, locatario1, 60, 4, 3, "Lugar aconchegante, mas difícil acesso.")
    create_reservation_with_review(imovel4, locatario2, 15, 2, 5, "Perfeito para viagens rápidas!")

    db.session.commit()

    print("Banco populado com sucesso ✅")
