'''A module for testing registration, login, reset password and
logout
'''
import unittest
import json
from app import create_app
from app import db


class RegistrationLoginTokenTestCase(unittest.TestCase):
    '''A class for that instantiates a client for testing and has functions
    for testing that the registration, login logout and reseting password work
    '''

    def setUp(self):
        '''A method to set up an instance of a client to test'''
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.information = {
            'user_email': 'user1@gmail.com',
            'user_password': 'password'
        }

        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def register_one_user(self):
        '''A method that registers one user'''
        result_of_post_method = self.client().post('/auth/register', data=self.information)
        return result_of_post_method

    def test_register_endpoint(self):
        '''A happy path to test registration with right information'''
        post_result = self.register_one_user()
        result = json.loads(post_result.data.decode())
        self.assertIn("Email and password entered correctly", result['message'])
        self.assertEqual(post_result.status_code, 201)

    def test_similar_users(self):
        '''A method to test no registration when the user had been registered
        before
        '''
        post_result = self.register_one_user()
        self.assertEqual(post_result.status_code, 201)
        second_similar_post = self.register_one_user()
        result = json.loads(second_similar_post.data.decode())
        self.assertEqual(result['message'], 'The user email entered already exists!')
        self.assertEqual(second_similar_post.status_code, 409)

    def test_the_user_login(self):
        '''A method to thest that login works happy path and returns right variables'''
        post_result = self.register_one_user()
        self.assertEqual(post_result.status_code, 201)
        result_of_post_method = self.client().post('/auth/login', data=self.information)
        result = json.loads(result_of_post_method.data.decode())
        self.assertEqual(result['message'], 'User logged in')
        self.assertNotEqual(result['access-token'], None)
        self.assertEqual(result_of_post_method.status_code, 200)

    def test_non_registereduser(self):
        '''A method to test that a user cannot login with a wrong email'''
        user_data = {
            'user_email':'unknown_email@gmail.com',
            'user_password':'password'
        }
        result_of_post_method = self.client().post('/auth/login', data=user_data)
        result = json.loads(result_of_post_method.data.decode())
        self.assertEqual(result['message'],
                         'User email does not exist! Register or check the '
                         'user email entered again.')
        self.assertEqual(result_of_post_method.status_code, 401)

    def test_wrong_password(self):
        '''A method to test that a user cannot login by inserting a wrong password
        to his email address that had been registered
        '''
        post_result = self.register_one_user()
        self.assertEqual(post_result.status_code, 201)
        user_data = {
            'user_email':'user1@gmail.com',
            'user_password': 'wrong_password'
        }
        result_of_post_method = self.client().post('/auth/login', data=user_data)
        result = json.loads(result_of_post_method.data.decode())
        self.assertEqual(result['message'], 'Wrong password entered for the user user1@gmail.com !')
        self.assertEqual(result_of_post_method.status_code, 401)

    def test_reset_password(self):
        '''A method to test that the password is reset when all values inserted are
        right
        '''
        post_result = self.register_one_user()
        self.assertEqual(post_result.status_code, 201)
        result_of_login = self.client().post('/auth/login', data=self.information)
        self.assertEqual(result_of_login.status_code, 200)
        token = json.loads(result_of_login.data.decode())['access-token']
        reset_data = {
            'user_password':'password',
            'new_password':'new_test_password',
            'verify_new_password': 'new_test_password'
        }
        result_of_post_method = self.client().post('auth/reset-password',
                                                   headers=dict(Authorization='Bearer '+ token),
                                                   data=reset_data
                                                  )

        self.assertEqual(result_of_post_method.status_code, 201)
        self.assertIn('Password reset', str(result_of_post_method.data))

    def test_reset_password_sad_path(self):
        '''A method to test that the reset password does not work when the
        wrong password has been used
        '''
        post_result = self.register_one_user()
        self.assertEqual(post_result.status_code, 201)
        result_of_login = self.client().post('/auth/login', data=self.information)
        self.assertEqual(result_of_login.status_code, 200)
        token = json.loads(result_of_login.data.decode())['access-token']
        reset_data = {
            'user_password':'wrongpassword',
            'new_password':'new_test_password',
            'verify_new_password': 'new_test_password'
        }
        result_of_post_method = self.client().post('auth/reset-password',
                                                   headers=dict(Authorization='Bearer '+ token),
                                                   data=reset_data
                                                  )
        self.assertEqual(result_of_post_method.status_code, 400)
        self.assertIn('Wrong password entered', str(result_of_post_method.data))

    def test_reset_password_sad_path_1(self):
        '''A method to test that reset password cannot work when the new password
        does not match the verify new password
        '''
        post_result = self.register_one_user()
        self.assertEqual(post_result.status_code, 201)
        result_of_login = self.client().post('/auth/login', data=self.information)
        self.assertEqual(result_of_login.status_code, 200)
        token = json.loads(result_of_login.data.decode())['access-token']
        reset_data = {
            'user_password':'password',
            'new_password':'new_test_password',
            'verify_new_password': 'wrong_new_test_password'
            }
        result_of_post_method = self.client().post('auth/reset-password',
                                                   headers=dict(Authorization='Bearer '+ token),
                                                   data=reset_data
                                                  )
        self.assertEqual(result_of_post_method.status_code, 400)
        self.assertIn('New password and verify new password do not match',
                      str(result_of_post_method.data))
