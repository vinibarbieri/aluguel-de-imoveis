# backend/models/review.py

from app import db

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservation.id'), unique=True)
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)

    reservation = db.relationship('Reservation', backref='review')
