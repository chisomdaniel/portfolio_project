# message_api.py
from flask_restful import Resource
from flasgger import swag_from

class MessageResource(Resource):
    @swag_from('path/to/swagger/message_get.yml')
    def get(self, message_id):
        # Your logic to retrieve and return message details
        pass
