from sqlalchemy.orm import relationship
from datetime import datetime

from . import db

class BaseModel:

    def serialize(self):
        new_dict = self.__dict__.copy()

        for key, value in new_dict.items():
            if isinstance(value, datetime):
                # Serialize datetime objects to string format
                new_dict[key] = value.strftime('%Y-%m-%d %H:%M:%S')

        if new_dict.get('_sa_instance_state', False):
            del new_dict['_sa_instance_state']

        return new_dict


# User Model
class User(db.Model, BaseModel):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # landlord or renter
    profile_image = db.Column(db.String(255))
    timestamps = db.Column(db.DateTime, default=datetime.utcnow)

    '''def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'type': self.type,
            'profile_image': self.profile_image,
            'timestamps': self.timestamps.strftime('%Y-%m-%d %H:%M:%S') if self.timestamps else None
        }'''

    # # User has many listings
    listings = relationship('RentalListing', backref='owner', lazy=True)

    # # User has many leases
    leases = relationship('Lease', backref='user', lazy=True)

    # # User has many reviews
    reviews = relationship('Review', backref='user', lazy=True)


# Rental Listing Model
class RentalListing(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    min_rent = db.Column(db.Float, nullable=False)
    max_rent = db.Column(db.Float, nullable=False)
    images = db.Column(db.JSON)  # Array of image URLs
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    rented = db.Column(db.Boolean, default=False)
    timestamps = db.Column(db.DateTime, default=datetime.utcnow)

    # # Rental Listing belongs to an owner (User)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # # Rental Listing has many leases
    leases = relationship('Lease', backref='listing', lazy=True)

    # # Rental Listing has many reviews
    reviews = relationship('Review', backref='listing', lazy=True)


# Lease Model
class Lease(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    monthly_rent = db.Column(db.Float, nullable=False)
    terms = db.Column(db.String(255))
    timestamps = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Boolean, default=0) # 0 = pending, 1 = accepted, 2 = running

    # # Lease belongs to a user (renter)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # # Lease belongs to a listing
    listing_id = db.Column(db.Integer, db.ForeignKey('rental_listing.id'), nullable=False)

    # # Lease has many payments
    payments = relationship('Payment', backref='lease', lazy=True)


# Payment Model
class Payment(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    comments = db.Column(db.String(255))
    timestamps = db.Column(db.DateTime, default=datetime.utcnow)

    # # Payment belongs to a lease
    lease_id = db.Column(db.Integer, db.ForeignKey('lease.id'), nullable=False)

    # # Payment has a payer (User)
    payer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)


# Review Model
class Review(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    stars = db.Column(db.Integer, nullable=False)
    body = db.Column(db.Text)
    timestamps = db.Column(db.DateTime, default=datetime.utcnow)

    # # Review belongs to a user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # # Review belongs to a listing
    listing_id = db.Column(db.Integer, db.ForeignKey('rental_listing.id'), nullable=False)


