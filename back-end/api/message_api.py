# message_api.py
from flask_restful import Resource
from flasgger import swag_from

class MessageResource(Resource):
    def get(self, message_id):
        # Your logic to retrieve and return message details
        pass
