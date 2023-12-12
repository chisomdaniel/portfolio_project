import os
import bcrypt

from flask import Flask, jsonify, request
from flask_restful import Api
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger, swag_from
from flask_jwt_extended import JWTManager

from config import DevelopmentConfig
from dotenv import load_dotenv

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

load_dotenv()  # Load environment variables

db = SQLAlchemy()
swagger = Swagger()
api = Api()
admin = Admin()
jwt = JWTManager()

def init_app():
    """Creating the core app"""

    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    # Initialize SQLAlchemy
    db.init_app(app)
    swagger.init_app(app)
    api.init_app(app)
    admin.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        from .models import User, RentalListing, Lease, Payment, Review, Message, Chat

        # Initialize the Admin page

        # Add views for each model to the admin page
        admin.add_view(ModelView(User, db.session))
        admin.add_view(ModelView(RentalListing, db.session))
        admin.add_view(ModelView(Lease, db.session))
        admin.add_view(ModelView(Payment, db.session))
        admin.add_view(ModelView(Review, db.session))
        admin.add_view(ModelView(Message, db.session))
        admin.add_view(ModelView(Chat, db.session))

        # Handle the home route
        @app.route('/')
        @swag_from('../static/swagger/home_get.yml')
        def home():
            return jsonify(
                {
                    "status": True,
                    "message": "Welcome to Flask API"
                }
            )


        # Your existing User model and db initialization code

        @app.route('/login', methods=['POST'])
        @swag_from('../static/swagger/login.yml')
        def login():
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')

            user = User.query.filter_by(email=email).first()

            try:
                password_correct = bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))
            except Exception as exc:
                return jsonify({
                    "message": "Invalid credentials",
                    "error": str(exc)
                })

            if user and password_correct:
                access_token = create_access_token(identity=user.id)
                return jsonify(access_token=access_token), 200
            else:
                return jsonify({"msg": "Invalid credentials"}), 401

        # db.drop_all()
        db.create_all()

        return app

if __name__ == '__main__':
    app = init_app()
    app.run(debug=True)
