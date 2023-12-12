# payment_api.py
from flask_restful import Resource
from flasgger import swag_from

class PaymentResource(Resource):
    def get(self, payment_id):
        # Your logic to retrieve and return payment details
        pass
