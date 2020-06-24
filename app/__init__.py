from flask import Flask
from config import app_config
#from flask_cors import CORS, cross_origin
from flask_migrate import Migrate
from app.models import *
#from .cart import cart as cart_blueprint



def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    #CORS(app)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    db.init_app(app)
    migrate = Migrate(app, db)

    
    #app.register_blueprint(cart_blueprint, url_prefix='/cart')
    

    return app