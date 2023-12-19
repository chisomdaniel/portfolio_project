from flask_restful import Api

api = Api()

from .user_api import UserResource, UserListResource
from .rental_listing_api import RentalListingResource, RentalListingListResource
from .lease_api import LeaseResource, LeaseListResource
from .payment_api import PaymentResource, PaymentListResource
from .review_api import ReviewResource, ReviewListingResource
from .image_api import ImageUploadResource
from .search_api import SearchResource

# Import and aapi.add_resource(UserResource, '/user/<int:user_id>')dd your API views

api.add_resource(UserResource, '/user/<int:user_id>', strict_slashes=False)
api.add_resource(UserListResource, '/users', strict_slashes=False)

api.add_resource(RentalListingResource, '/rental-listing/<int:listing_id>', strict_slashes=False)
api.add_resource(RentalListingListResource,  '/rental-listings', strict_slashes=False)


api.add_resource(LeaseResource, '/lease/<int:lease_id>', strict_slashes=False)
api.add_resource(LeaseListResource, '/leases', strict_slashes=False)

api.add_resource(PaymentResource, '/payment/<int:payment_id>', strict_slashes=False)
api.add_resource(PaymentListResource, '/payments', strict_slashes=False)

api.add_resource(ReviewResource, '/review/<int:review_id>', strict_slashes=False)
api.add_resource(ReviewListingResource, '/reviews', strict_slashes=False)

api.add_resource(ImageUploadResource, '/image', strict_slashes=False)

api.add_resource(SearchResource, '/search/<string:model_name>', strict_slashes=False)