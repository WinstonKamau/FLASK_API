'''A module to test the Bucket List class on crud for activities in a
bucketlist
'''
import unittest
import json
from app import create_app, db

class TheActivitiesTestCase(unittest.TestCase):
    '''A class for testing the CRUD for activities in a bucket list'''

    def setUp(self):
        '''Initialising the app and variables for testing'''
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.bucketlist = {"name": "Adventure"}
        self.activity = {"activity_name": "Climb the Himalayas"}
        self.user_information = {
            "user_email": "user1@gmail.com",
            "user_password": "password"
            }

        with self.app.app_context():
            db.create_all()
    
    def register_login_and_return_token(self):
        '''A method that registers a user, logs in a user, creates a token
        for the user and returns it'''
        self.client().post('/auth/register', data=self.user_information)
        result_of_login = self.client().post('/auth/login', data=self.user_information)
        token = json.loads(result_of_login.data.decode())['access-token']
        return token

    def post_a_bucket(self):
        '''A method that posts a bucket to the test_db, ideally all other
        methods use it so it acts as a method for posting for tests below.
        The method posts after registering and logging in
        '''
        return self.client().post('/bucketlists/',
                                  headers=dict(Authorization='Bearer '
                                               + self.register_login_and_return_token()
                                              ),
                                  data=self.bucketlist
                                 )

    def test_activity_creation(self):
        """A method to test that the API creates an activity"""
        post_bucket_data = self.post_a_bucket()
        self.assertEqual(post_bucket_data.status_code, 201)
        json_data = json.loads(post_bucket_data.data.decode('utf-8').replace("'", "\""))
        result_of_post_activity = self.client().post('/bucketlists/{}/items/'.format(json_data['id']),
                                                     headers=dict(Authorization='Bearer '
                                                                  + self.register_login_and_return_token()
                                                                  ),
                                                     data=self.activity)
        self.assertEqual(result_of_post_activity.status_code, 201)
    
    def tearDown(self):
        '''A method for removing all set variables and deleting our database'''
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    #def test_read_bucket(self):
        """A method to test that the api reads activiies"""
        #result_of_post_activity = self.client().post('/bucketlists/0/items/', data=self.activity)
        #self.assertEqual(result_of_post_activity.status_code, 201)
        #result_of_get_activity = self.client().get('/bucketlists/')
        #self.assertEqual(result_of_get_method.status_code, 200)
        #self.assertIn('Climb the Himalayas', str(result_of_get_method.data))