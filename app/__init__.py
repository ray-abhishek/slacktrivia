from flask import Flask
from config import app_config
from flask_cors import CORS
from flask_migrate import Migrate
from app.models import *
from .slash import slash as slash_blueprint



def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    db.init_app(app)
    migrate = Migrate(app, db)

    
    app.register_blueprint(slash_blueprint, url_prefix='/slash')
    

    return app