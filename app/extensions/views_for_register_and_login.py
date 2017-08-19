from . import registration_login_blueprint
import re
from flask.views import MethodView
from flask import make_response, request, jsonify
from app.models import User


class Registration(MethodView):

    def post(self):
        if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', request.data['user_email']):
            user = User.query.filter_by(user_email=request.data['user_email']).first()
            if not user:
                
                data_posted = request.data
                user_email = data_posted['user_email']
                try:
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
                    'message':'The user email entered already exists!'
                }

                return make_response(jsonify(response)), 202
        else:
            response = {
                'message': 'The user email entered is not valid ensure it has @ and .'
            }
            return make_response(jsonify(response)), 400

class Login(MethodView):
    def post(self):
        if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', request.data['user_email']):
            user = User.query.filter_by(user_email=request.data['user_email']).first()
            post_data = request.data
            if user:
                if user.password_confirm(post_data['user_password']):
                    token = user.create_encoded_token(user.id)
                    if token:
                        response = {
                            'message': 'User logged in',
                            'access-token': token.decode()
                        }
                        return make_response(jsonify(response)), 200
                else:
                    response = {
                        'message': 'Wrong password entered for the user %s !'%(request.data['user_email'])
                    }
                    return make_response(jsonify(response)), 401   
            else:
                response = {
                    'message': 'Username does not exist! Register or check the username entered again.'
                }
                return make_response(jsonify(response)), 401
        else:
            response = {
                'message': 'The user email entered is not valid ensure it has @ and .'
            }
            return make_response(jsonify(response)), 400


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