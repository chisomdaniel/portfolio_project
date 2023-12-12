from app import init_app
from api import api  

app = init_app()
api.init_app(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
