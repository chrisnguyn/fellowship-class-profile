import os

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app(init_db=False):
    app = Flask(__name__, template_folder='./templates')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    app.config['SECRET_KEY'] = 'this-really-needs-to-be-changed'

    db.init_app(app)

    if init_db:
        db.create_all(app=app)

    from web.app import bp
    app.register_blueprint(bp)
    CORS(app)

    return app
