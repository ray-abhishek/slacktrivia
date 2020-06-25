from flask import Blueprint

sendquiz = Blueprint('sendquiz', __name__)

from . import functions