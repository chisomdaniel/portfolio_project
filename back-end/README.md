# The Backend
This backend is built using Flask to serve the front-end of the rental app.

To run it:
1. Ensure you have python, pip and MySQL installed on your machine.
1. Get the directory locally and run `pip install -r requirements.txt` to get the dependencies installed locally.
1. Configure your .env file in the root directory. An example is below:
```
SECRET_KEY=23578g29h293r8h29402490
DEBUG=True
SQLALCHEMY_TRACK_MODIFICATIONS=False
SQLALCHEMY_DATABASE_URI=mysql+pymysql://<username>:<password>@localhost/<database-name>
JWT_ACCESS_TOKEN_EXPIRES=86400  # 24 hours in seconds
UPLOADED_PHOTOS_DEST=static/uploads/
```
1. Run the start script to start the application: `python run.py`
1. Access the app using `127.0.0.1:5000` on your browser.

### Flasgger
This API is continuously documented using Flasgger(Swagger for flask).
To access the API documentation, run the app locally then access `127.0.0.1:5000/apidocs` on your browser.
