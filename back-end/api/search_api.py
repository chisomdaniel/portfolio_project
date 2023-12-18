from flask_restful import Resource, reqparse
from flask import jsonify, current_app, make_response
from sqlalchemy import or_
from app.models import User

from flask_jwt_extended import jwt_required
from flasgger import swag_from
from app import models

class SearchResource(Resource):
    # @jwt_required()
    @swag_from('../static/swagger/search_get.yml')  # Add Swagger documentation
    def get(self, model_name):
        # Define a parser for query parameters
        parser = reqparse.RequestParser()
        parser.add_argument('query', type=str, help='Search query', required=True, location='args')
        parser.add_argument('column', type=str, help='Column to search in', location='args')
        args = parser.parse_args()

        # Import a model class based on the given model_name
        model_class = getattr(models, model_name, None) 

        print("-------------------------------------------------------")
        print(f"Args: {model_class}")

        if not model_class or model_class is None:
            response_data = {"message": "Model not found"}
            response = make_response(jsonify(response_data), 404)
            return response

        # Validate the provided column exists in the model
        if args['column'] and args['column'] not in model_class.__table__.columns.keys():
            response_data = {"message": "Invalid column"}
            response = make_response(jsonify(response_data), 400)
            return response

        # Build the query using 'or_' to search across the specified column
        search_column = args['column'] if args['column'] else model_class.__table__.columns.keys()
        search_query = or_(*[getattr(model_class, search_column).ilike(f"%{args['query']}%")])

        # Execute the query
        results = model_class.query.filter(search_query).all()

        # Serialize the results
        serialized_results = [result.serialize() for result in results]

        print(serialized_results)

        response_data = {"results": serialized_results}
        response = make_response(jsonify(response_data), 200)

        return response
