# app/resources.py
from flask_restful import Resource, reqparse, abort
from flask import jsonify, url_for
from flask_jwt_extended import jwt_required
from flasgger import swag_from

from app.models import User
from app import db

import bcrypt

class UserResource(Resource):
    @swag_from('../static/swagger/user_get.yml')
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        
        return jsonify(user.serialize())

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

        return jsonify(user.serialize())

    @swag_from('../static/swagger/user_delete.yml')
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204  # No content

class UserListResource(Resource):
    @swag_from('../static/swagger/users_get.yml')
    def get(self):
        users = User.query.all()
        return jsonify([user.serialize() for user in users])

    @swag_from('../static/swagger/users_post.yml')
    def post(self):
        print('here 0')
        try:
            parser = reqparse.RequestParser() # Formats and Validates the request
            parser.add_argument('name', type=str, required=True, help='Username is required')
            parser.add_argument('email', type=str, required=True, help='Email is required')
            parser.add_argument('password', type=str, required=True, help='Email is required')
            parser.add_argument('type', type=str, default='tenant', required=True, help='Type is required')
            args = parser.parse_args()
            password_text = args['password']
        
            hashed_pw = bcrypt.hashpw(password_text.encode('utf-8'), bcrypt.gensalt())
            args['password'] = hashed_pw

            new_user = User(**args)
            db.session.add(new_user)
            db.session.commit()

            return jsonify({
                "message": f"User {new_user.email} created successfully"
            })
        except Exception as exc:
            return {
                "error": str(exc),
                "message": "Error creating user"
            }

