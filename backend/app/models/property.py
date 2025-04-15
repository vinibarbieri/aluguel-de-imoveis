from app import db

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    price_per_day = db.Column(db.Float, nullable=False)
    available_from = db.Column(db.Date, nullable=False)
    available_until = db.Column(db.Date, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User', backref='properties', lazy=True)  # Relacionamento com User
    image_url = db.Column(db.String(255), nullable=True)
    
    reservations = db.relationship('Reservation', backref='property_listing', lazy=True)  # Mudança aqui para 'property_listing'
    
    def __repr__(self):
        return f'<Property {self.title}>'
