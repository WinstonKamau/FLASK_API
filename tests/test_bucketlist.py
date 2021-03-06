'''A module to test the Bucket List class on crud for bucketlists '''
import unittest
import json
from app import create_app, db

class TheBucketTestCase(unittest.TestCase):
    '''A class to test the functionalities of creating reading updating and deleting a
    bucketlist'''

    def setUp(self):
        '''Initialising the app and variables for testing'''
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.bucketlist = {"name": "Climb the Himalayas"}
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
        The method posts after registering and logging in
        '''
        return self.client().post('/bucketlists/',
                                  headers=dict(Authorization='Bearer '
                                               + self.token()
                                              ),
                                  data=self.bucketlist
                                 )

    def test_bucketlist_creation(self):
        """A method to test that the API creates a bucket"""
        post_data = self.post_a_bucket()
        self.assertEqual(post_data.status_code, 201)
        self.assertIn('Climb the Himalayas', str(post_data.data))

    def test_wrong_keys_provided(self):
        '''Posting a path with wrong key and no key name provided'''
        wrong_key = {'wrong_key': 'Travel'}
        result_of_wrong_key = self.client().post('/bucketlists/',
                                                 headers=dict(Authorization='Bearer '
                                                              + self.token()
                                                             ),
                                                 data=wrong_key
                                                )
        self.assertEqual(result_of_wrong_key.status_code, 400)
        self.assertIn('The key variable name', str(result_of_wrong_key.data))
        result_of_wrong_key_2 = self.client().post('/bucketlists/',
                                                   headers=dict(Authorization='Bearer '
                                                                + self.token()
                                                               ))
        self.assertEqual(result_of_wrong_key_2.status_code, 400)

    def test_if_bucket_already_exists(self):
        '''A method to test that creation does not happen if the bucket
        already exists
        '''
        post_data = self.post_a_bucket()
        self.assertEqual(post_data.status_code, 201)
        post_data_second_time = self.post_a_bucket()
        self.assertEqual(post_data_second_time.status_code, 409)
        self.assertIn('A bucket list exists with a similar name of',
                      str(post_data_second_time.data))

    def test_read_bucket(self):
        """A method to test that the api reads a bucket"""
        post_data = self.post_a_bucket()
        self.assertEqual(post_data.status_code, 201)
        result_of_get_method = self.client().get('/bucketlists/',
                                                 headers=dict(Authorization='Bearer '
                                                              + self.token())
                                                )
        self.assertEqual(result_of_get_method.status_code, 200)
        self.assertIn('Climb the Himalayas', str(result_of_get_method.data))


    def test_read_bucket_using_id(self):
        '''A method to test the retrieval of one bucket using an id placed in brackets
        on the after the '/bucketlists/' statement below
        '''
        post_data = self.post_a_bucket()
        self.assertEqual(post_data.status_code, 201)
        #converting the response from posting to json format
        json_data = json.loads(post_data.data.decode('utf-8').replace("'", "\""))
        final_data = self.client().get('/bucketlists/{}'.format(json_data['id']),
                                       headers=dict(Authorization='Bearer '
                                                    + self.token())
                                      )
        self.assertEqual(final_data.status_code, 200)
        self.assertIn('Climb the Himalayas', str(final_data.data))

    def test_read_bucket_using_q(self):
        '''Test read bucket using q with bucket existing'''
        post_data = self.post_a_bucket()
        self.assertEqual(post_data.status_code, 201)
        post_data_2 = self.client().post('/bucketlists/',
                                         headers=dict(Authorization='Bearer '
                                                      + self.token()),
                                         data={"name": "Family"})
        self.assertEqual(post_data_2.status_code, 201)
        result_of_get_method = self.client().get("/bucketlists/?q=Climb the Himalayas",
                                                 headers=dict(Authorization='Bearer '
                                                              + self.token())
                                                )
        self.assertEqual(result_of_get_method.status_code, 200)
        self.assertIn("Climb the Himalayas", str(result_of_get_method.data))
        self.assertNotIn('Family', str(result_of_get_method.data))

    def test_q_no_item(self):
        '''A method to test reading a bucket using q where the bucket does not
        exist
        '''
        post_data = self.post_a_bucket()
        self.assertEqual(post_data.status_code, 201)
        result_of_get_method = self.client().get("/bucketlists/?q=aisdo",
                                                 headers=dict(Authorization='Bearer '
                                                              + self.token())
                                                )
        self.assertEqual(result_of_get_method.status_code, 200)
        self.assertIn('Name does not exist', str(result_of_get_method.data))

    def test_read_bucket_using_limit(self):
        '''A method to test reading a bucket using correct inputs'''
        post_data = self.post_a_bucket()
        self.assertEqual(post_data.status_code, 201)
        post_data_2 = self.client().post('/bucketlists/',
                                         headers=dict(Authorization='Bearer '
                                                      + self.token()),
                                         data={"name": "Family"})
        self.assertEqual(post_data_2.status_code, 201)
        post_data_3 = self.client().post('/bucketlists/',
                                         headers=dict(Authorization='Bearer '
                                                      + self.token()),
                                         data={"name": "Travel"})
        self.assertEqual(post_data_3.status_code, 201)
        post_data_4 = self.client().post('/bucketlists/',
                                         headers=dict(Authorization='Bearer '
                                                      + self.token()),
                                         data={"name": "Adventure"})
        self.assertEqual(post_data_4.status_code, 201)
        post_data_5 = self.client().post('/bucketlists/',
                                         headers=dict(Authorization='Bearer '
                                                      + self.token()),
                                         data={"name": "Acts of Kindness"})
        self.assertEqual(post_data_5.status_code, 201)
        result_of_get_method = self.client().get('/bucketlists/?limit=3',
                                                 headers=dict(Authorization='Bearer '
                                                              + self.token())
                                                )
        self.assertEqual(result_of_get_method.status_code, 200)
        self.assertIn('Family', str(result_of_get_method.data))
        self.assertIn('Travel', str(result_of_get_method.data))
        self.assertIn('Climb the Himalayas', str(result_of_get_method.data))
        self.assertNotIn('Adventure', str(result_of_get_method.data))
        self.assertNotIn('Acts of Kindness', str(result_of_get_method.data))

    def test_limit_zero(self):
        '''Test reading bucket using a limit for zero'''
        post_data = self.post_a_bucket()
        self.assertEqual(post_data.status_code, 201)
        post_data_2 = self.client().post('/bucketlists/',
                                         headers=dict(Authorization='Bearer '
                                                      + self.token()),
                                         data={"name": "Family"})
        self.assertEqual(post_data_2.status_code, 201)
        post_data_3 = self.client().post('/bucketlists/',
                                         headers=dict(Authorization='Bearer '
                                                      + self.token()),
                                         data={"name": "Travel"})
        self.assertEqual(post_data_3.status_code, 201)
        post_data_4 = self.client().post('/bucketlists/',
                                         headers=dict(Authorization='Bearer '
                                                      + self.token()),
                                         data={"name": "Adventure"})
        self.assertEqual(post_data_4.status_code, 201)
        post_data_5 = self.client().post('/bucketlists/',
                                         headers=dict(Authorization='Bearer '
                                                      + self.token()),
                                         data={"name": "Acts of Kindness"})
        self.assertEqual(post_data_5.status_code, 201)
        result_of_get_method = self.client().get('/bucketlists/?limit=0',
                                                 headers=dict(Authorization='Bearer '
                                                              + self.token())
                                                )
        self.assertEqual(result_of_get_method.status_code, 200)
        self.assertIn('Zero returns no buckets', str(result_of_get_method.data))

    def test_over_limit(self):
        '''A method to test reading bucket by inserting a limit that is
        over the values in it'''
        post_data = self.post_a_bucket()
        self.assertEqual(post_data.status_code, 201)
        post_data_2 = self.client().post('/bucketlists/',
                                         headers=dict(Authorization='Bearer '
                                                      + self.token()),
                                         data={"name": "Family"})
        self.assertEqual(post_data_2.status_code, 201)
        post_data_3 = self.client().post('/bucketlists/',
                                         headers=dict(Authorization='Bearer '
                                                      + self.token()),
                                         data={"name": "Travel"})
        self.assertEqual(post_data_3.status_code, 201)
        post_data_4 = self.client().post('/bucketlists/',
                                         headers=dict(Authorization='Bearer '
                                                      + self.token()),
                                         data={"name": "Adventure"})
        self.assertEqual(post_data_4.status_code, 201)
        post_data_5 = self.client().post('/bucketlists/',
                                         headers=dict(Authorization='Bearer '
                                                      + self.token()),
                                         data={"name": "Acts of Kindness"})
        self.assertEqual(post_data_5.status_code, 201)
        result_of_get_method = self.client().get('/bucketlists/?limit=7',
                                                 headers=dict(Authorization='Bearer '
                                                              + self.token())
                                                )
        self.assertEqual(result_of_get_method.status_code, 200)
        self.assertIn('Family', str(result_of_get_method.data))
        self.assertIn('Travel', str(result_of_get_method.data))
        self.assertIn('Climb the Himalayas', str(result_of_get_method.data))
        self.assertIn('Adventure', str(result_of_get_method.data))
        self.assertIn('Acts of Kindness', str(result_of_get_method.data))

    def test_edit_bucketlist(self):
        """A method to test the editing of a bucket list"""
        post_data = self.post_a_bucket()
        self.assertEqual(post_data.status_code, 201)
        result_of_put_method = self.client().put(
            '/bucketlists/1',
            headers=dict(Authorization='Bearer '
                         + self.token()
                        ),
            data={
                "name": "The seasons will be, summer winter and autumn"
            })
        self.assertEqual(result_of_put_method.status_code, 201)
        result_of_get_method = self.client().get('/bucketlists/1',
                                                 headers=dict(Authorization='Bearer '
                                                              + self.token())
                                                )
        self.assertIn('The seasons will b', str(result_of_get_method.data))

    def test_edit_bucketlist_sad_path_1(self):
        '''Test edit bucket using a name already stored'''
        post_data = self.post_a_bucket()
        self.assertEqual(post_data.status_code, 201)
        result_of_put_method = self.client().put(
            '/bucketlists/1',
            headers=dict(Authorization='Bearer '
                         + self.token()
                        ),
            data={
                "name": "Climb the Himalayas"
            })
        self.assertEqual(result_of_put_method.status_code, 409)

    def test_delete_bucketlist(self):
        """A method to test the deleting of a bucket list"""
        post_data = self.post_a_bucket()
        self.assertEqual(post_data.status_code, 201)
        result_of_delete_method = self.client().delete('/bucketlists/1',
                                                       headers=dict(Authorization='Bearer '
                                                                    + self.token())
                                                      )
        self.assertEqual(result_of_delete_method.status_code, 200)
        response_after_removal = self.client().get('/bucketlists/1',
                                                   headers=dict(Authorization='Bearer '
                                                                + self.token())
                                                  )
        self.assertEqual(response_after_removal.status_code, 400)

    def tearDown(self):
        '''A method for removing all set variables and deleting our database'''
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
