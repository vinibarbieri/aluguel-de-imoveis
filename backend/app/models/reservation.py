from app import db
from datetime import date

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    renter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    approved = db.Column(db.Boolean, default=False)
    
    renter = db.relationship('User', backref='reservations', lazy=True)

    def __repr__(self):
        return f'<Reservation {self.id}>'
