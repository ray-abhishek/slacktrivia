from flask import Flask
from config import app_config
#from flask_cors import CORS
from flask_migrate import Migrate
from app.models import *
from .sendquiz import sendquiz as sendquiz_blueprint



def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    #CORS(app)
    print(config_name," is config_name")
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    db.init_app(app)
    migrate = Migrate(app, db)

    
    app.register_blueprint(sendquiz_blueprint, url_prefix='/sendquiz')
    

    return app