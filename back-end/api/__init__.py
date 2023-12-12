from flask_restful import Api

api = Api()

from .user_api import UserResource, UserListResource
from .rental_listing_api import RentalListingResource
from .lease_api import LeaseResource
from .payment_api import PaymentResource
from .review_api import ReviewResource
from .message_api import MessageResource
from .chat_api import ChatResource

# Import and aapi.add_resource(UserResource, '/user/<int:user_id>')dd your API views

api.add_resource(UserResource, '/user/<int:user_id>')
api.add_resource(UserListResource, '/users')
api.add_resource(RentalListingResource, '/rental-listing/<int:listing_id>')
api.add_resource(LeaseResource, '/lease/<int:lease_id>')
api.add_resource(PaymentResource, '/payment/<int:payment_id>')
api.add_resource(ReviewResource, '/review/<int:review_id>')
api.add_resource(MessageResource, '/message/<int:message_id>')
api.add_resource(ChatResource, '/chat/<int:chat_id>')
