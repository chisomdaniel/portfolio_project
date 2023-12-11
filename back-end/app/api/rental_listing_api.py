# rental_listing_api.py
from flask_restful import Resource
from flasgger import swag_from

class RentalListingResource(Resource):
    @swag_from('path/to/swagger/rental_listing_get.yml')
    def get(self, listing_id):
        # Your logic to retrieve and return rental listing details
        pass
