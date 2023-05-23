import os

import boto3
from flask import Flask, send_from_directory
from flask import make_response
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint

from app.conf.config import Config
from app.database import database
from app.movies.movies import movies_bp
from app.users.users import users_bp

app = Flask(__name__)


@app.route('/')
def home_page():
    return make_response('Hello From Homepage.', 200)


# Swagger api docs route
@app.route("/swagger/<path:path>")
def specs():
    return send_from_directory(os.getcwd(), "swagger.json")


def initialize_app():
    app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
    JWTManager(app)
    ddb_client = boto3.client('dynamodb', region_name=Config.REGION_NAME)
    database.users(ddb_client)
    database.movies(ddb_client)
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.json'
    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Microservices Movie Application"
        })
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
    app.register_blueprint(movies_bp)
    app.register_blueprint(users_bp)
    return app


if __name__ == '__main__':
    flask_app = initialize_app()
    flask_app.run(host='0.0.0.0', port=Config.APP_PORT, debug=True)
