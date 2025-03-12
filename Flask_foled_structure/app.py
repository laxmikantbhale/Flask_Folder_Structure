from flask import Flask, render_template
from flask_jwt_extended import JWTManager

from config import Config
from db import db, init_db
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
import jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    #initilize JWT
    jwt_manager = JWTManager(app)

    #initilize DB
    init_db(app)

    #register blueprint
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix="/api")

    return app






if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)