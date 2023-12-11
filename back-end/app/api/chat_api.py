# chat_api.py
from flask_restful import Resource
from flasgger import swag_from

class ChatResource(Resource):
    @swag_from('path/to/swagger/chat_get.yml')
    def get(self, chat_id):
        # Your logic to retrieve and return chat details
        pass
