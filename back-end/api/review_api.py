from flask import request, jsonify, make_response
from flask_restful import Resource, reqparse
from flasgger import swag_from
from flask_jwt_extended import jwt_required

from app.models import Review
from app import db

class ReviewResource(Resource):
    # @jwt_required()
    @swag_from('../static/swagger/review_get.yml') 
    def get(self, review_id):
        review = Review.query.get(review_id)

        if not review:
            response_data = {"message": "Review not found"}
            response = make_response(jsonify(response_data), 404)
            return response

        # Serialize the review data 
        serialized_review = review.serialize()

        response_data = serialized_review
        response = make_response(jsonify(response_data), 200)
        return response

    # @jwt_required()
    @swag_from('../static/swagger/review_patch.yml')  # Add Swagger documentation
    def patch(self, review_id):
        # Parse and validate the request data
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, help='Updated review title')
        parser.add_argument('stars', type=int, help='Updated review stars')
        parser.add_argument('body', type=str, help='Updated review body')
        args = parser.parse_args()

        review = Review.query.get(review_id)

        if not review:
            response_data = {"message": "Review not found"}
            response = make_response(jsonify(response_data), 404)

            return response

        # Update review attributes based on provided data
        if args['title']:
            review.title = args['title']
        if args['stars']:
            review.stars = args['stars']
        if args['body']:
            review.body = args['body']

        # Commit changes to the database
        db.session.commit()

        # Serialize the updated review data
        serialized_review = review.serialize()

        response_data = {"message": "Review updated successfully", "review": serialized_review}
        response = make_response(jsonify(response_data), 200)

        return response

    # @jwt_required()
    @swag_from('../static/swagger/review_delete.yml')  # Add Swagger documentation
    def delete(self, review_id):
        review = Review.query.get(review_id)

        if not review:
            response_data = {"message": "Review not found"}
            response = make_response(jsonify(response_data), 404)

            return response

        # Delete the review from the database
        db.session.delete(review)
        db.session.commit()

        response_data = {"message": "Review deleted successfully"}
        response = make_response(jsonify(response_data), 204)

        return response



class ReviewListingResource(Resource):
    # @jwt_required()
    @swag_from('../static/swagger/reviews_get.yml')  # Add Swagger documentation
    def get(self, review_id):
        # Your logic to retrieve and return review details
        review = Review.query.get(review_id)

        if not review:
            response_data = {"message": "Review not found"}
            response = make_response(jsonify(response_data), 404)

            return response

        # Serialize the review data
        serialized_review = review.serialize()

        response_data = serialized_review
        response = make_response(jsonify(response_data), 200)

        return response


    # @jwt_required()
    @swag_from('../static/swagger/reviews_post.yml')  # Add Swagger documentation
    def post(self):
        # Parse and validate the request data
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, help='Review title', required=True)
        parser.add_argument('stars', type=int, help='Review stars', required=True)
        parser.add_argument('body', type=str, help='Review body')
        parser.add_argument('user_id', type=int, help='ID of the user submitting the review', required=True)
        parser.add_argument('listing_id', type=int, help='ID of the listing associated with the review', required=True)
        args = parser.parse_args()

        # Create a new Review instance
        new_review = Review(**args)

        # Add the new review to the database
        db.session.add(new_review)
        db.session.commit()

        # Serialize the new review data
        serialized_review = new_review.serialize()

        response_data = {"message": "Review created successfully", "review": serialized_review}
        response = make_response(jsonify(response_data), 201)
        return response