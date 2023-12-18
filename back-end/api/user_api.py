# app/resources.py
from flask_restful import Resource, reqparse, abort
from flask import jsonify, url_for, make_response
from flask_jwt_extended import jwt_required
from flasgger import swag_from

from app.models import User
from app import db

import bcrypt

class UserResource(Resource):
    @swag_from('../static/swagger/user_get.yml')
    def get(self, user_id):
        user = User.query.get_or_404(user_id)

        # Serialize user information
        serialized_user = user.serialize()

        # Serialize user's leases
        serialized_leases = [lease.serialize() for lease in user.leases]

        # Serialize user's listings
        serialized_listings = [listing.serialize() for listing in user.listings]

        # Serialize user's reviews
        serialized_reviews = [review.serialize() for review in user.reviews]

        serialized_user.update({
            "leases": serialized_leases,
            "listings": serialized_listings,
            "reviews": serialized_reviews,
        })

        response_data = {serialized_user}
        response = make_response(jsonify(response_data), 200)
        return response


    @swag_from('../static/swagger/user_put.yml')
    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()

        user = User.query.get_or_404(user_id)

        if args['username']:
            user.name = args['username']
        if args['email']:
            user.email = args['email']
        if args['password']:
            password_text = args['password']
            hashed_pw = bcrypt.hashpw(password_text.encode('utf-8'), bcrypt.gensalt())
            user.password = hashed_pw

        db.session.commit()

        response_data = {user.serialize()}
        response = make_response(jsonify(response_data), 200)

        return response 

    @swag_from('../static/swagger/user_delete.yml')
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()

        response_data = {"message": f"User ID: {user.id} deleted successfully."}
        response = make_response(jsonify(response_data), 204)
        return response

class UserListResource(Resource):
    @swag_from('../static/swagger/users_get.yml')
    def get(self):
        users = User.query.all()

        response_data = {jsonify([user.serialize() for user in users])}
        response = make_response(jsonify(response_data), 200)
        return response

    @swag_from('../static/swagger/users_post.yml')
    def post(self):
        try:
            parser = reqparse.RequestParser() # Formats and Validates the request
            parser.add_argument('name', type=str, required=True, help='Username is required')
            parser.add_argument('email', type=str, required=True, help='Email is required')
            parser.add_argument('password', type=str, required=True, help='Email is required')
            parser.add_argument('type', type=str, default='tenant', required=False, help='Type is required')
            parser.add_argument('profile_image', type=str, required=False, help='Image not provided')
            args = parser.parse_args()
            password_text = args['password']
        
            hashed_pw = bcrypt.hashpw(password_text.encode('utf-8'), bcrypt.gensalt())
            args['password'] = hashed_pw

            new_user = User(**args)
            db.session.add(new_user)
            db.session.commit()

            response_data = {"message": f"User {new_user.email} created successfully"}
            response = make_response(jsonify(response_data), 201)
            return response
        
        except Exception as exc:
            response_data = {
                "error": str(exc),
                "message": "Error creating user"
            }
            response = make_response(jsonify(response_data), 500)
            return response

