from app import db
from app.models.review import Review  

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'))
    renter_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    approved = db.Column(db.Boolean, default=None)  # None = pendente

    property = db.relationship('Property', backref='reservations')
    renter = db.relationship('User', backref='reservations')
