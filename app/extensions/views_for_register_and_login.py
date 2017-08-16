from . import registration_login_blueprint

from flask.views import MethodView
from flask import make_response, request, jsonify
from app.models import User


class Registration(MethodView):

    def post(self):
        user = User.query.filter_by(user_email=request.data['user_email']).first()

        if not user:
            try:
                data_posted = request.data
                user_email = data_posted['user_email']
                user_password = data_posted['user_password']
                user = User(user_email=user_email, user_password=user_password)
                user.save_user()
                response = {
                    'message': 'Email and password entered correctly. Use them to log in'
                }
                return make_response(jsonify(response)), 201
            except Exception as e:
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 401
        
        else:
            response = {
                'message':'The user email entered already exists. '
            }

            return make_response(jsonify(response)), 202


class Login(MethodView):
    def post(self):
        user = User.query.filter_by(user_email=request.data['user_email']).first()
        post_data = request.data
        if user:
            if user.password_confirm(post_data['user_password']):
                token = user.create_encoded_token(user.id)
                response = {
                    'message': 'User logged in',
                    'access-token': user.decode_token_to_sub(token) 
                }
                return make_response(jsonify(response)), 200
            else:
                response = {
                    'message': 'Wrong password entered'
                }
                return make_response(jsonify(response)), 401   
        else:
            response = {
                'message': 'Wrong user name entered'
            }
            return make_response(jsonify(response)), 401







view_for_registration = Registration.as_view('register_view')

registration_login_blueprint.add_url_rule(
    '/auth/register',
    view_func=view_for_registration,
    methods=['POST'])

view_for_login = Login.as_view('login_view')

registration_login_blueprint.add_url_rule(
    '/auth/login',
    view_func=view_for_login,
    methods=['POST']
)