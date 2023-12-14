# rental_listing_api.py
from flask_restful import Resource, reqparse, abort
from flask import jsonify
from flasgger import swag_from
from app.models import RentalListing

class RentalListingResource(Resource):

    @swag_from('../static/swagger/rental_get.yml')
    def get(self, listing_id=None):
        # Your logic to retrieve and return rental listing details
        if listing_id:
            rental = RentalListing.query.get_or_404(listing_id)
            return jsonify(rental.serialize())
        
        rentals = RentalListing.query.all()
        return jsonify([rental.serialize for rental in rentals])
    
    def post(self):

        try:
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, required=True, help='Rental name required')
            parser.add_argument('location', type=str, required=True, help='Location required')
            parser.add_argument('min-rent', type=float, required=True, help='Minimum rent required')
            parser.add_argument('max-rent', type=float, required=True, help='Maximum rent name required')
            parser.add_argument('rented', type=bool, required=True, help='Rent status required')
            parser.add_argument('owner_id', type=int, required=True, help='Owner ID required')

            args = parser.parse_args()
            new_rental = RentalListing()
        except Exception as e:
            return {
                'error': str(e),
                'message': 'Error creating listing'
            }

