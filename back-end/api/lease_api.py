# lease_api.py
from flask_restful import Resource
from flasgger import swag_from
from flask_jwt_extended import jwt_required

class LeaseResource(Resource):
    def get(self, lease_id):
        # Your logic to retrieve and return lease details
        pass
