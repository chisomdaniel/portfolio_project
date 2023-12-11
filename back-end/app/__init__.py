import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

from sqlalchemy import inspect

from config import DevelopmentConfig
from dotenv import load_dotenv

load_dotenv() # Load enviroment variables

env = os.environ.get('FLASK_ENV', 'dev')

app = Flask(__name__, instance_relative_config=False)
app.config.from_object(DevelopmentConfig)

# Initialize SQLAlchemy
db = SQLAlchemy(app)
from app.models import User, RentalListing, Lease, Payment, Review, Message, Chat

# Initialize the Admin page
admin = Admin(app, name='Rental Housing Admin', template_mode='bootstrap3')

# Add views for each model to the admin page
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(RentalListing, db.session))
admin.add_view(ModelView(Lease, db.session))
admin.add_view(ModelView(Payment, db.session))
admin.add_view(ModelView(Review, db.session))
admin.add_view(ModelView(Message, db.session))
admin.add_view(ModelView(Chat, db.session))

# Initialize Swagger
swagger = Swagger(app)

# Import and add your API views
from app.api.user_api import UserResource
from app.api.user_api import UserListResource
from app.api.rental_listing_api import RentalListingResource
from app.api.lease_api import LeaseResource
from app.api.payment_api import PaymentResource
from app.api.review_api import ReviewResource
from app.api.message_api import MessageResource
from app.api.chat_api import ChatResource

api = Api(app)

api.add_resource(UserResource, '/user')
api.add_resource(UserListResource, '/users')
api.add_resource(RentalListingResource, '/rental-listing')
api.add_resource(LeaseResource, '/lease')
api.add_resource(PaymentResource, '/payment')
api.add_resource(ReviewResource, '/review')
api.add_resource(MessageResource, '/message')
api.add_resource(ChatResource, '/chat')

# Handle the home route
@app.route('/')
def home():
    return jsonify(
        {
            "status": True,
            "message": "Welcome to Flask API"
        }
    )

if __name__ == '__main__':
    try:
        db.create_all()
    except Exception as exc:
        print(exc)
    app.run(debug=True)
