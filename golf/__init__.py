import os

from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv, dotenv_values

load_dotenv()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.split(CURRENT_DIR)[0]
ENV_PATH = os.path.join(BASE_DIR, '.env')

# DB params
DB_NAME = dotenv_values(ENV_PATH)['DB_NAME']
DB_PASSWORD = dotenv_values(ENV_PATH)['DB_PASSWORD']
HOST = dotenv_values(ENV_PATH)['HOST']
PORT = dotenv_values(ENV_PATH)['PORT']
USERNAME = dotenv_values(ENV_PATH)['USERNAME']
USING_DB = dotenv_values(ENV_PATH)['USING_DB']
USING_DIALECT = dotenv_values(ENV_PATH)['USING_DIALECT']

# golf params
SECRET_KEY = dotenv_values(ENV_PATH)['SECRET_KEY']


# app create
def create_app():
    app = Flask(__name__)
    app.static_folder = os.path.join(CURRENT_DIR, 'static')
    app.secret_key = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = f"{USING_DB}+{USING_DIALECT}://{USERNAME}:{DB_PASSWORD}@{HOST}:{PORT}" \
                                            f"/{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    from .models import db
    db.init_app(app)
    # with app.app_context():
    #     db.create_all()

    return app


app = create_app()

# login manager settings
login_manager = LoginManager()
login_manager.init_app(app)

from .endpoints import *
