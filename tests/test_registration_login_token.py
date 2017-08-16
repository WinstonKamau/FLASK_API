import unittest
import json
from app import create_app
from app import db


class RegistrationLoginTokenTestCase(unittest.TestCase):


    def setUp(self):
        self.app = create_app(config_name = 'testing')
        self.client = self.app.test_client
        self.information = {
            'user_email': 'user1@gmail.com',
            'user_password': 'password'
        }

        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_the_register_endpoint_function(self):
        result_of_post_method = self.client().post('/auth/register', data=self.information)
        result = json.loads(result_of_post_method.data.decode())
        self.assertIn("Email and password entered correctly", result['message'])
        self.assertEqual(result_of_post_method.status_code, 201)

    def test_null_registration_of_users_with_same_info(self):
        result_of_post_method = self.client().post('/auth/register', data=self.information)
        self.assertEqual(result_of_post_method.status_code, 201)
        result_of_post_method_2 = self.client().post('/auth/register', data=self.information)
        result = json.loads(result_of_post_method_2.data.decode())
        self.assertEqual(result['message'], 'The user email entered already exists. ')
        self.assertEqual(result_of_post_method_2.status_code, 202)

    def test_the_user_login(self):
        result_of_post_method = self.client().post('/auth/register', data=self.information)
        self.assertEqual(result_of_post_method.status_code, 201)
        result_of_post_method = self.client().post('/auth/login', data=self.information)
        result = json.loads(result_of_post_method.data.decode())
        self.assertEqual(result['message'], 'User logged in')
        self.assertEqual(result_of_post_method.status_code, 200)

    def test_non_registered_user_login_with_wrong_user_email(self):
        user_data = {
            'user_email':'unknown_email@gmail.com',
            'user_password':'password'
        }
        result_of_post_method = self.client().post('/auth/login', data=user_data)
        result = json.loads(result_of_post_method.data.decode())
        self.assertEqual(result['message'], 'Wrong user name entered')
        self.assertNotEqual(result['access_token'], None)
        self.assertEqual(result_of_post_method.status_code, 401)

    def test_resgistered_user_with_wrong_password(self):
        result_of_post_method = self.client().post('/auth/register', data=self.information)
        self.assertEqual(result_of_post_method.status_code, 201)
        user_data = {
            'user_email':'user1@gmail.com',
            'user_password': 'wrong_password'
        }
        result_of_post_method = self.client().post('/auth/login', data=user_data)
        result = json.loads(result_of_post_method.data.decode())
        self.assertEqual(result['message'], 'Wrong password entered')
        self.assertEqual(result_of_post_method.status_code, 401)



