# lease_api.py
from flask_restful import Resource
from flasgger import swag_from

class LeaseResource(Resource):
    @swag_from('path/to/swagger/lease_get.yml')
    def get(self, lease_id):
        # Your logic to retrieve and return lease details
        pass
