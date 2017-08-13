from flask import Blueprint

registration_login_blueprint = Blueprint('author', __name__)

from . import views_for_register_and_login