from flask import Blueprint

# Create the blueprint
main = Blueprint('main', __name__, template_folder='templates')

from . import routes
