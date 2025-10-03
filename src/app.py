from flask import Flask
from flasgger import Swagger
from src.api.api_rooms import rooms_bp

app = Flask(__name__)
swagger = Swagger(app)

app.register_blueprint(rooms_bp)

if __name__ == '__main__':
    app.run(debug=True)