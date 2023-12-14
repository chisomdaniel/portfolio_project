# rental_listing_api.py
from flask_restful import Resource
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

