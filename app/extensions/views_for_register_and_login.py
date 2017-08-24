from . import registration_login_blueprint
import re
from flask.views import MethodView
from flask import make_response, request, jsonify
from app.models import User
from flask_bcrypt import Bcrypt


class Registration(MethodView):

    def post(self):
        user_email_status = str(request.data.get('user_email', ''))
        user_password_status = str(request.data.get('user_password', ''))
        if not user_email_status or not user_password_status:
            response = jsonify({
                'message': "Key variables to be entered are supposed to be 'user_email' and 'user_password'"
            })
            return make_response(response), 400
        if not re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', request.data['user_email']):
            response = {
                    'message': 'The user email entered is not valid ensure it has @ and .'
                }
            return make_response(jsonify(response)), 400
        if User.query.filter_by(user_email=request.data['user_email']).first():
            response = {
                    'message':'The user email entered already exists!'
                }
            return make_response(jsonify(response)), 409
        else:
            user = User.query.filter_by(user_email=request.data['user_email']).first()
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
        

class Login(MethodView):
    def post(self):
        user_email_status = str(request.data.get('user_email', ''))
        user_password_status = str(request.data.get('user_password', ''))
        if not user_email_status or not user_password_status:
            response = jsonify({
                'message': "Key variables to be entered are supposed to be 'user_email' and 'user_password'"
            })
            return make_response(response), 400
        if not re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', request.data['user_email']):
            response = {
                    'message': 'The user email entered is not valid ensure it has @ and .'
                }
            return make_response(jsonify(response)), 400
        if not User.query.filter_by(user_email=request.data['user_email']).first():
            response = {
                'message': 'User email does not exist! Register or check the user email entered again.'
            }
            return make_response(jsonify(response)), 401
        else:
            user = User.query.filter_by(user_email=request.data['user_email']).first()
            post_data = request.data
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



class ResetPassword(MethodView):
    def post(self):
        header = request.headers.get('Authorization')
        if not header:
                response = jsonify({
                    'message': 'No authorisation header given'
                })
                return make_response(response), 401    
        if ' ' not in header:
            response= jsonify({
                'message1': 'A space needs to exist between the Bearer and token.',
                'message2': 'The authorization should be typed as the example below',
                'example': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MDMzNDUzMjIsInN1YiI6MiwiaWF0IjoxNTAzMzQxNzIyfQ.fCZ3ibX-vHQ5SKxYbrarQ0I8lvq5TgMt03A5vGlGhDE"'
            })
            return make_response(response), 401
        user_id = User.decode_token_to_sub(header)
        if not isinstance(user_id, int):
            response = jsonify({
                    'message': 'Invalid token entered'
                })
            return make_response(response), 401
        if 'user_password' not in request.data.keys():
            response = jsonify({
                'message': "To reset password the variable 'user_password' for the current password needs to be inserted"
            })
            return make_response (response), 400
        if 'new_password' not in request.data.keys():
            response = jsonify({
                    'message': "The key 'new_password' has not been entered"
                })
            return make_response(response), 400
        if 'verify_new_password' not in request.data.keys():
            response = jsonify({
                'message': "The key 'verify_new_password' has not been entered" 
            })
            return make_response(response), 400
        if not request.data.get('new_password') == request.data.get('verify_new_password'):
            response = jsonify({
                    'message': 'New password and verify new password do not match'
                    })
            return make_response(response), 400 
        if not User.query.filter_by(id=user_id).first().password_confirm(request.data.get('user_password')):
            response = jsonify({
                'message': 'Wrong password entered for the user'
            })
            return make_response(response), 400
        else:
            current_password = request.data.get('user_password')
            user = User.query.filter_by(id=user_id).first()
            new_password = request.data.get('new_password')
            verify_new_password = request.data.get ('verify_new_password')
            user.user_password = Bcrypt().generate_password_hash(new_password).decode()
            user.save_user()
            response = jsonify({
                'user_email': user.user_email,
                'user_password': user.user_password,
                'message': 'Password reset'
            })
            return make_response (response), 201                               

class Logout(MethodView):
    def get(self):
        '''A method to delete the token on the client's browser needs to be added
        and the response below given
        '''
        response = jsonify({
            'message': 'Logged out'
        })
        return make_response(response), 200

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

view_for_logout = Logout.as_view('logout_view')

registration_login_blueprint.add_url_rule(
    '/auth/logout',
    view_func=view_for_logout,
    methods=['GET']
)