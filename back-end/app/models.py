from sqlalchemy.orm import relationship
from datetime import datetime

from app import db

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # landlord or renter
    profile_image = db.Column(db.String(255))
    timestamps = db.Column(db.DateTime, default=datetime.utcnow)

    # # User has many listings
    # listings = relationship('RentalListing', backref='owner', lazy=True)

    # # User has many leases
    # leases = relationship('Lease', backref='user', lazy=True)

    # # User has many reviews
    # reviews = relationship('Review', backref='user', lazy=True)

    # # User has many sent messages
    # sent_messages = relationship('Message', foreign_keys='Message.sender', backref='sender', lazy=True)

    # # User has many received messages
    # received_messages = relationship('Message', foreign_keys='Message.recipient', backref='recipient', lazy=True)


# Rental Listing Model
class RentalListing(db.Model):
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
    # leases = relationship('Lease', backref='listing', lazy=True)

    # # Rental Listing has many reviews
    # reviews = relationship('Review', backref='listing', lazy=True)

    # # Rental Listing has many messages (Chat)
    # chats = relationship('Chat', backref='listing', lazy=True)


# Lease Model
class Lease(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    monthly_rent = db.Column(db.Float, nullable=False)
    terms = db.Column(db.String(255))
    timestamps = db.Column(db.DateTime, default=datetime.utcnow)

    # # Lease belongs to a user (renter)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # # Lease belongs to an owner (User)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # # Lease belongs to a listing
    listing_id = db.Column(db.Integer, db.ForeignKey('rental_listing.id'), nullable=False)

    # # Lease has many payments
    # payments = relationship('Payment', backref='lease', lazy=True)


# Payment Model
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    comments = db.Column(db.String(255))
    timestamps = db.Column(db.DateTime, default=datetime.utcnow)

    # # Payment belongs to a lease
    lease_id = db.Column(db.Integer, db.ForeignKey('lease.id'), nullable=False)

    # # Payment has a payer (User)
    payer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# Review Model
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    stars = db.Column(db.Integer, nullable=False)
    body = db.Column(db.Text)
    timestamps = db.Column(db.DateTime, default=datetime.utcnow)

    # # Review belongs to a user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # # Review belongs to a listing
    listing_id = db.Column(db.Integer, db.ForeignKey('rental_listing.id'), nullable=False)


# Message Model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamps = db.Column(db.DateTime, default=datetime.utcnow)

    # # Message belongs to a chat
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)

    # # Message has a sender (User)
    sender = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # # Message has a recipient (User)
    recipient = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    

# Chat Model
class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamps = db.Column(db.DateTime, default=datetime.utcnow)

    # Chat belongs to a listing
    listing_id = db.Column(db.Integer, db.ForeignKey('rental_listing.id'), nullable=False)

    # Chat has many messages
    # messages = relationship('Message', backref='chat', lazy=True)

