from flask import Blueprint

registration_login_blueprint = Blueprint('auth', __name__)

from . import views_for_register_and_login