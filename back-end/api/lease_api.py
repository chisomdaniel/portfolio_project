from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from flasgger import swag_from
from flask_jwt_extended import jwt_required

from app.models import Lease
from app import db

class LeaseResource(Resource):
    # @jwt_required()
    @swag_from('../static/swagger/lease_get.yml')  # Add Swagger documentation
    def get(self, lease_id):
        # Parse and validate the lease_id from the request
        parser = reqparse.RequestParser()
        parser.add_argument('lease_id', type=int, help='Lease ID', required=True)
        args = parser.parse_args()

        lease_id = args['lease_id']

        # Retrieve the lease from the database
        lease = Lease.query.get(lease_id)

        if not lease:
            response_data = {"message": "Lease not found"}
            response = make_response(jsonify(response_data), 404)

            return response

        # Serialize the lease object into a dictionary
        lease_data = lease.serialize()
        lease_data.update({
            'payments': [payment.id for payment in lease.payments],  # Example: Get payment IDs
        })
        
        lease_data.update({"message": "Lease Found"})
        response_data = {lease_data}
        response = make_response(jsonify(response_data), 200)

        return response

    # @jwt_required()
    @swag_from('../static/swagger/lease_patch.yml')  # Add Swagger documentation
    def patch(self, lease_id):
        # Parse and validate the lease_id from the request
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, help='Lease title')
        parser.add_argument('monthly_rent', type=float, help='Monthly rent')
        parser.add_argument('terms', type=str, help='Lease terms')
        parser.add_argument('status', type=bool, help='Lease status (0 = pending, 1 = accepted, 2 = running)')
        args = parser.parse_args()

        lease_id = lease_id
        lease = Lease.query.get(lease_id)

        if not lease:
            response_data = {"message": "Lease not found"}
            response = make_response(jsonify(response_data), 404)

            return response

        # Update lease attributes based on provided data
        if args['title']:
            lease.title = args['title']
        if args['monthly_rent']:
            lease.monthly_rent = args['monthly_rent']
        if args['terms']:
            lease.terms = args['terms']
        if args['status'] is not None:
            lease.status = args['status']

        # Commit changes to the database
        db.session.commit()

        response_data = {"message": "Lease updated successfully"}
        response = make_response(jsonify(response_data), 200)

        return response
    

    # @jwt_required()
    @swag_from('../static/swagger/lease_delete.yml')  # Add Swagger documentation
    def delete(self, lease_id):
        lease = Lease.query.get(lease_id)

        if not lease:
            response_data = {"message": "Lease not found"}
            response = make_response(jsonify(response_data), 404)

            return response

        # Delete the lease from the database
        db.session.delete(lease)
        db.session.commit()

        response_data = {"message": "Lease deleted successfully"}
        response = make_response(jsonify(response_data), 204)

        return response

class LeaseListResource(Resource):
    # @jwt_required()
    @swag_from('../static/swagger/leases_get.yml')  # Add Swagger documentation
    def get(self, lease_id):
        leases = Lease.query.all()
        return [lease.serialize() for lease in leases]
    
    # @jwt_required()
    @swag_from('../static/swagger/lease_post.yml')  # Add Swagger documentation
    def post(self):
        # Parse and validate the request data
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, help='Lease title', required=True)
        parser.add_argument('monthly_rent', type=float, help='Monthly rent', required=True)
        parser.add_argument('terms', type=str, help='Lease terms', required=False)
        parser.add_argument('status', type=bool, help='Lease status (0 = pending, 1 = accepted, 2 = running)', default=0)
        parser.add_argument('user_id', type=int, help='User ID (renter)', required=True)
        parser.add_argument('listing_id', type=int, help='Listing ID', required=True)
        args = parser.parse_args()

        # Create a new Lease instance
        new_lease = Lease(**args)

        # Add the new lease to the database
        db.session.add(new_lease)
        db.session.commit()

        response_data = {"message": "Lease created successfully", "lease_id": new_lease.id}
        response = make_response(jsonify(response_data), 201)
        return response
