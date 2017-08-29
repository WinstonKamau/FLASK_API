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

    def token(self):
        '''A method that registers a user, logs in a user, creates a token
        for the user and returns it'''
        self.client().post('/auth/register', data=self.user_information)
        result_of_login = self.client().post('/auth/login', data=self.user_information)
        token = json.loads(result_of_login.data.decode())['access-token']
        return token

    def post_a_bucket(self):
        '''A method that posts a bucket to the test_db, ideally all other
        methods use it so it acts as a method for posting for tests below.
        The method posts after registering and logging in and returns json
        data for posting an activity
        '''
        post_bucket_data = self.client().post('/bucketlists/',
                                              headers=dict(Authorization='Bearer '
                                                           + self.token()
                                                          ),
                                              data=self.bucketlist
                                             )
        json_data = json.loads(post_bucket_data.data.decode('utf-8').replace("'", "\""))
        return json_data

    def post_an_activity(self):
        '''A method that posts and activity and returns the response'''
        bucket_json_data = self.post_a_bucket()
        return self.client().post('/bucketlists/{}/items/'.format(bucket_json_data['id']),
                                  headers=dict(Authorization='Bearer '
                                               + self.token()
                                              ),
                                  data=self.activity)

    def test_activity_creation(self):
        """A method to test that the API creates an activity"""
        post_activity_data = self.post_an_activity()
        self.assertEqual(post_activity_data.status_code, 201)
        self.assertIn('Climb the Himalayas', str(post_activity_data.data))

    def test_conflict_on_creation(self):
        '''A method to test that activity is not created if it already exists'''
        post_activity_data = self.post_an_activity()
        self.assertEqual(post_activity_data.status_code, 201)
        post_activity_data_second_time = self.client().post('/bucketlists/1/items/',
                                                            headers=dict(Authorization='Bearer '
                                                                         + self.token()
                                                                        ),
                                                            data=self.activity)
        self.assertEqual(post_activity_data_second_time.status_code, 409)


    def test_getting_all_activitites(self):
        '''A method to test that the API gets back all activities'''
        post_activity_data = self.post_an_activity()
        self.assertEqual(post_activity_data.status_code, 201)
        result_of_get_activity = self.client().get('/bucketlists/1/items/',
                                                   headers=dict(Authorization='Bearer '
                                                                + self.token()
                                                               ),
                                                  )
        self.assertEqual(result_of_get_activity.status_code, 200)
        self.assertIn('Climb the Himalayas', str(result_of_get_activity.data))

    def test_get_activity__id(self):
        '''A method to test getting an activity by providing the id of the activity'''
        post_activity_data = self.post_an_activity()
        self.assertEqual(post_activity_data.status_code, 201)
        second_activity = {"activity_name": "Climb Mt. Kilimanjaro"}
        post_activity_data_2 = self.client().post('/bucketlists/1/items/',
                                                  headers=dict(Authorization='Bearer '
                                                               + self.token()
                                                              ),
                                                  data=second_activity)
        self.assertEqual(post_activity_data_2.status_code, 201)
        result_of_get_activity_1 = self.client().get('/bucketlists/1/items/1',
                                                     headers=dict(Authorization='Bearer '
                                                                  + self.token()
                                                                 ),
                                                    )
        self.assertEqual(result_of_get_activity_1.status_code, 200)
        self.assertIn('Climb the Himalayas', str(result_of_get_activity_1.data))            
        result_of_get_activity_2 = self.client().get('/bucketlists/1/items/2',
                                                     headers=dict(Authorization='Bearer '
                                                                  + self.token()
                                                                 )
                                                    )
        self.assertEqual(result_of_get_activity_1.status_code, 200)
        self.assertIn('Climb Mt. Kilimanjaro', str(result_of_get_activity_2.data))

    def test_q_search(self):
        '''Test getting back an activity using q for search happy path with activity exsiting'''
        post_activity_data = self.post_an_activity()
        self.assertEqual(post_activity_data.status_code, 201)
        second_activity = {"activity_name": "Climb Mt. Kilimanjaro"}
        post_activity_data_2 = self.client().post('/bucketlists/1/items/',
                                                  headers=dict(Authorization='Bearer '
                                                               + self.token()
                                                              ),
                                                  data=second_activity)
        self.assertEqual(post_activity_data_2.status_code, 201)
        result_of_get_activity = self.client().get('bucketlists/1/items/?q=Climb Mt. Kilimanjaro',
                                                   headers=dict(Authorization='Bearer '
                                                                + self.token()
                                                               )
                                                  )
        self.assertEqual(result_of_get_activity.status_code, 200)
        self.assertIn('Climb Mt. Kilimanjaro', str(result_of_get_activity.data))
        self.assertNotIn('Climb the Himalayas', str(result_of_get_activity.data))

    def test_non_activity_search(self):
        '''Test the response if a non-existent activity is searched for'''
        post_activity_data = self.post_an_activity()
        self.assertEqual(post_activity_data.status_code, 201)
        result_of_get_activity = self.client().get('bucketlists/1/items/?q=Climb Mt. Kilimanjaro',
                                                   headers=dict(Authorization='Bearer '
                                                                + self.token()
                                                               )
                                                  )
        self.assertEqual(result_of_get_activity.status_code, 200)
        self.assertIn('The activity name does not exist', str(result_of_get_activity.data))

    def test_get_activity_limit(self):
        '''A method to test the limit variable on happy path'''
        post_activity_data = self.post_an_activity()
        self.assertEqual(post_activity_data.status_code, 201)
        second_activity = {"activity_name": "Climb Mt. Kilimanjaro"}
        third_activity = {"activity_name": "Climb the Alps"}
        fourth_activity = {"activity_name": "Climb Mt. Everest"}
        post_activity_data_2 = self.client().post('/bucketlists/1/items/',
                                                  headers=dict(Authorization='Bearer '
                                                               + self.token()
                                                              ),
                                                  data=second_activity)
        self.assertEqual(post_activity_data_2.status_code, 201)
        post_activity_data_2 = self.client().post('/bucketlists/1/items/',
                                                  headers=dict(Authorization='Bearer '
                                                               + self.token()
                                                              ),
                                                  data=third_activity)
        self.assertEqual(post_activity_data_2.status_code, 201)
        post_activity_data_2 = self.client().post('/bucketlists/1/items/',
                                                  headers=dict(Authorization='Bearer '
                                                               + self.token()
                                                              ),
                                                  data=fourth_activity)
        self.assertEqual(post_activity_data_2.status_code, 201)
        result_of_get_activity = self.client().get('bucketlists/1/items/?limit=2',
                                                   headers=dict(Authorization='Bearer '
                                                                + self.token()
                                                               )
                                                  )
        self.assertEqual(result_of_get_activity.status_code, 200)
        self.assertIn('Climb the Himalayas', str(result_of_get_activity.data))
        self.assertIn('Climb Mt. Kilimanjaro', str(result_of_get_activity.data))
        self.assertNotIn('Climb the Alps', str(result_of_get_activity.data))
        self.assertNotIn('Climb Mt. Everest', str(result_of_get_activity.data))
        result_of_get_activity_1 = self.client().get('bucketlists/1/items/?limit=0',
                                                     headers=dict(Authorization='Bearer '
                                                                  + self.token()
                                                                 )
                                                    )
        self.assertEqual(result_of_get_activity_1.status_code, 200)
        self.assertNotIn('Climb the Himalayas', str(result_of_get_activity_1.data))
        self.assertNotIn('Climb Mt. Kilimanjaro', str(result_of_get_activity_1.data))
        self.assertNotIn('Climb the Alps', str(result_of_get_activity_1.data))
        self.assertNotIn('Climb Mt. Everest', str(result_of_get_activity_1.data))
        self.assertIn('Zero returns no item', str(result_of_get_activity_1.data))

    def test_updating_an_activity(self):
        '''A method to test updating an activity happy path with correct
        details
        '''
        post_activity_data = self.post_an_activity()
        self.assertEqual(post_activity_data.status_code, 201)
        update_activity = {"activity_name": "Climb Mt. Kilimanjaro"}
        result_of_put = self.client().put('/bucketlists/1/items/1',
                                          headers=dict(Authorization='Bearer '
                                                       + self.token()),
                                          data=update_activity
                                         )
        self.assertEqual(result_of_put.status_code, 200)
        self.assertIn('Climb Mt. Kilimanjaro', str(result_of_put.data))

    def test_update_similar_activity(self):
        '''Test that an activity is not updated if it already exists'''
        post_activity_data = self.post_an_activity()
        self.assertEqual(post_activity_data.status_code, 201)
        update_activity = {"activity_name": "Climb the Himalayas"}
        result_of_put = self.client().put('/bucketlists/1/items/1',
                                          headers=dict(Authorization='Bearer '
                                                       + self.token()),
                                          data=update_activity
                                         )
        self.assertEqual(result_of_put.status_code, 409)

    def test_deleting_an_activity(self):
        '''A method to test that deleting an activity works in happy path'''
        post_activity_data = self.post_an_activity()
        self.assertEqual(post_activity_data.status_code, 201)
        result_of_delete_activity = self.client().delete('bucketlists/1/items/1',
                                                         headers=dict(Authorization='Bearer '
                                                                      + self.token())
                                                        )
        self.assertEqual(result_of_delete_activity.status_code, 200)
        result_of_delete_activity_2 = self.client().delete('bucketlists/1/items/1',
                                                           headers=dict(Authorization='Bearer '
                                                                        + self.token())
                                                          )
        self.assertEqual(result_of_delete_activity_2.status_code, 400)

    def tearDown(self):
        '''A method for removing all set variables and deleting our database'''
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
