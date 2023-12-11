# app/resources.py
from flask_restful import Resource, reqparse, abort
from flask import jsonify, url_for
from app.models import User
from app import db

class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return jsonify(user.serialize())

    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        args = parser.parse_args()

        user = User.query.get_or_404(user_id)
        
        if args['username']:
            user.username = args['username']
        if args['email']:
            user.email = args['email']

        db.session.commit()

        return jsonify(user.serialize())

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204  # No content

class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        return jsonify([user.serialize() for user in users])

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='Username is required')
        parser.add_argument('email', type=str, required=True, help='Email is required')
        args = parser.parse_args()

        new_user = User(username=args['username'], email=args['email'])
        db.session.add(new_user)
        db.session.commit()

        return jsonify(new_user.serialize()), 201  # Created

