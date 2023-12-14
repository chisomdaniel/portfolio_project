# rental_listing_api.py
from flask_restful import Resource, reqparse, abort
from flask import jsonify
from flasgger import swag_from
from app.models import RentalListing
from app import db
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

class RentalListingResource(Resource):

    @swag_from('../static/swagger/rental_get.yml')
    def get(self, listing_id=None):
        '''Get a listing by the ID provided or all listing if no ID is provided'''
        # Your logic to retrieve and return rental listing details
        if listing_id:
            rental = RentalListing.query.get_or_404(listing_id)
            return jsonify(rental.serialize())
        
        rentals = RentalListing.query.all()
        return jsonify([rental.serialize() for rental in rentals])
    
    @jwt_required()
    @swag_from('../static/swagger/rental_post.yml')
    def post(self):
        '''create  a new listing'''
        try:
            user_id = get_jwt_identity()
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, required=True, help='Rental name required')
            parser.add_argument('location', type=str, required=True, help='Location required')
            parser.add_argument('min-rent', type=float, required=True, help='Minimum rent required')
            parser.add_argument('max-rent', type=float, required=True, help='Maximum rent name required')
            parser.add_argument('rented', type=bool, required=True, help='Rent status required')
            parser.add_argument('owner_id', type=int, default=user_id, required=True, help='Owner ID required')
            parser.add_argument('images', type=db.JSON, required=False, help='No image added')
            parser.add_argument('latitude', type=float, required=False, help='Latitude not provided')
            parser.add_argument('longitude', type=float, required=False, help='Longitude not provided')

            args = parser.parse_args()
            new_rental = RentalListing(**args)
            db.session.add(new_rental)
            db.session.commit()

        except Exception as e:
            return {
                'error': str(e),
                'message': 'Error creating listing'
            }
    
    @jwt_required()
    @swag_from('../static/swagger/rental_put.yml')
    def put(self, listing_id):
        '''create update listing'''
        try:
            user_id = get_jwt_identity()
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, required=False, help='Rental name required')
            parser.add_argument('location', type=str, required=False, help='Location required')
            parser.add_argument('min-rent', type=float, required=False, help='Minimum rent required')
            parser.add_argument('max-rent', type=float, required=False, help='Maximum rent name required')
            parser.add_argument('rented', type=bool, required=False, help='Rent status required')
            # parser.add_argument('owner_id', type=int, required=False, help='Owner ID required')
            parser.add_argument('images', type=db.JSON, required=False, help='No image added')
            parser.add_argument('latitude', type=float, required=False, help='Latitude not provided')
            parser.add_argument('longitude', type=float, required=False, help='Longitude not provided')

            args = parser.parse_args()

            listing = RentalListing.query.get_or_404(listing_id)
            if listing.owner_id == user_id:
                for key, value in listing.items():
                    setattr(listing, key, value)
                db.session.commit()
            else:
                abort(401), 'Unauthorized user'

        except Exception as e:
            return {
                'error': str(e),
                'message': 'Error updating listing'
            }

    @jwt_required()
    @swag_from('../static/swagger/rental_delete.yml')
    def delete(self, listing_id):
        '''Delete a listing'''
        user_id = get_jwt_identity()
        listing = RentalListing.query.get_or_404(listing_id)

        if listing.owner_id == user_id:
            db.session.delete(listing)
            db.session.commit()
            return '', 204

        return abort(401), 'Unauthorized user'

