from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from flasgger import swag_from
from flask_jwt_extended import jwt_required

from app.models import Payment
from app import db

class PaymentResource(Resource):
    # @jwt_required()
    @swag_from('../static/swagger/payment_get.yml')  # Add Swagger documentation
    def get(self, payment_id):
        if payment_id:
            payment = Payment.query.get_or_404(payment_id)
            response_data = payment.serialize()
            response = make_response(jsonify(response_data), 200)

            return response

        response_data = {
            "message": "Payment not Found"
        }
        response = make_response(jsonify(response_data), 404)

        return response

        

    # @jwt_required()
    @swag_from('../static/swagger/payment_patch.yml')  # Add Swagger documentation
    def patch(self, payment_id):
        # Parse and validate the payment_id from the request
        parser = reqparse.RequestParser()
        parser.add_argument('amount', type=float, help='Payment amount')
        parser.add_argument('comments', type=str, help='Payment comments')
        args = parser.parse_args()

        payment = Payment.query.get(payment_id)

        if not payment:
            response_data = {"message": "Payment not found"}
            response = make_response(jsonify(response_data), 404)

            return response

        # Update payment attributes based on provided data
        if args['amount']:
            payment.amount = args['amount']
        if args['comments']:
            payment.comments = args['comments']

        # Commit changes to the database
        db.session.commit()

        response_data = {"message": "Payment updated successfully"}
        response = make_response(jsonify(response_data), 200)

        return response

    # @jwt_required()
    @swag_from('../static/swagger/payment_delete.yml')  # Add Swagger documentation
    def delete(self, payment_id):
        payment = Payment.query.get(payment_id)

        if not payment:
            response_data = {"message": "Payment not found"}
            response = make_response(jsonify(response_data), 404)

            return response

        # Delete the payment from the database
        db.session.delete(payment)
        db.session.commit()

        response_data = {"message": "Payment deleted successfully"}
        response = make_response(jsonify(response_data), 200)

        return response
    
class PaymentListResource(Resource):
    # @jwt_required()
    @swag_from('../static/swagger/payment_post.yml')  # Add Swagger documentation
    def post(self):
        # Parse and validate the request data
        parser = reqparse.RequestParser()
        parser.add_argument('amount', type=float, help='Payment amount', required=True)
        parser.add_argument('comments', type=str, help='Payment comments')
        parser.add_argument('lease_id', type=int, help='Lease ID', required=True)
        parser.add_argument('payer_id', type=int, help='Payer ID (User)', required=True)
        args = parser.parse_args() 

        # Create a new Payment instance
        new_payment = Payment(**args)

        # Add the new payment to the database
        db.session.add(new_payment)
        db.session.commit()

        response_data = {"message": "Payment created successfully", "payment_id": new_payment.id}
        response = make_response(jsonify(response_data), 201)

        return response
    
    # @jwt_required()
    @swag_from('../static/swagger/payments_get.yml')  # Add Swagger documentation
    def get(self):
        payments = Payment.query.all()

        response_data = [payment.serialize() for payment in payments]
        response = make_response(jsonify(response_data), 200)
        return response