from flask import Blueprint

# Specify the template folder relative to this file
main = Blueprint('main', __name__, template_folder='templates')

from . import routes
