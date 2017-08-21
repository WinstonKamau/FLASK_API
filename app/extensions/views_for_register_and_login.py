from . import registration_login_blueprint
import re
from flask.views import MethodView
from flask import make_response, request, jsonify
from app.models import User
from flask_bcrypt import Bcrypt


class Registration(MethodView):

    def post(self):
        user_email_status = request.data['user_email']
        user_password_status = request.data['user_password']
        if user_email_status and user_password_status:
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
        else:
            response = jsonify({
                'message': "Key variables to be entered are supposed to be 'user_email' and 'user_password'"
            })
            return make_response(response), 400

class Login(MethodView):
    def post(self):
        user_email_status = request.data['user_email']
        user_password_status = request.data['user_password']
        if user_email_status and user_password_status:
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
        else:
            response = {
                'message': "Key variables to be entered are supposed to be user_email and user_password "
            }

class ResetPassword(MethodView):
    def post(self):
        header = request.headers.get('Authorization')
        if header:
            if ' ' in header:
                splitted_header = header.split(' ')
                token = splitted_header[1]
                user_id = User.decode_token_to_sub(token)
                if isinstance(user_id, int):
                    current_password = request.data.get('user_password')
                    if current_password:
                        user = User.query.filter_by(id=user_id).first()
                        if user.password_confirm(current_password):
                            new_password = request.data.get('new_password')
                            verify_new_password = request.data.get ('verify_new_password')
                            if new_password:
                                if verify_new_password:
                                    if new_password == verify_new_password:
                                        user.user_password = Bcrypt().generate_password_hash(new_password).decode()
                                        user.save_user()
                                        response = jsonify({
                                            'user_email': user.user_email,
                                            'user_password': user.user_password,
                                            'message': 'Password reset'
                                        })
                                        return make_response (response), 201
                                    else:
                                        response = jsonify({
                                            'message': 'Passwords do not match'
                                        })
                                        return make_response(response), 400
                                else:
                                    response = jsonify({
                                        'message': "The key 'verify_new_password' has not been entered" 
                                    })
                                    return make_response(response), 400
                            else:
                                response = jsonify({
                                    'message': "The key 'new_password' has not beek entered"
                                })                                
                        else:
                            response = jsonify({
                                'message': 'Wrong password entered'
                            })
                            return make_response(response), 400
                    else:
                        response = jsonify({
                            'message': "To reset password the variable 'current_password' needs to be inserted"
                        })
                        return make_response (response), 400
                else:
                    response = jsonify({
                        'message': 'Invalid token entered'
                    })
                    return make_response(response), 400
            else:
                response({
                    'message': 'A space needs to exist between the Bearer and token.'
                })
                return make_response(response), 400
        else:
            response = jsonify({
                'message': 'No authorisation header given'
            })
            return make_response(response), 401


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

view_for_reset_password = ResetPassword.as_view('reset_password_view')

registration_login_blueprint.add_url_rule(
    '/auth/reset-password',
    view_func=view_for_reset_password,
    methods=['POST']
)