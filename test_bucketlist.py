'''A module to test the Bucket List class on crud for bucketlists '''
import unittest
import os
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

        with self.app.app_context():
            db.create_all()

    def test_bucketlist_creation(self):
        """a method to test that the API creates a bucket"""
        result_of_post_method = self.client().post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(result_of_post_method.status_code, 201)
        self.assertIn('Climb the Himalayas', str(result_of_post_method.data))

    def test_read_bucket(self):
        """a method to test that the api reads a bucket"""
        result_of_post_method = self.client().post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(result_of_post_method.status_code, 201)
        result_of_get_method = self.client().get('/bucketlists/')
        self.assertEqual(result_of_get_method.status_code, 200)
        self.assertIn('Climb the Himalayas', str(result_of_get_method.data))


    def test_read_bucket_using_id(self):
        """a method to test the retrieval of one bucket using an id placed in brackets
        on the after the '/bucketlists/' statement below
        """
        #a method to post the dictionary "name": "Climb the Himalayas"
        result_of_post_method = self.client().post('/bucketlists/', data=self.bucketlist)
        #a method to test that the post worked
        self.assertEqual(result_of_post_method.status_code, 201)
        #converting the response from posting to json format
        json_data = json.loads(result_of_post_method.data.decode('utf-8').replace("'", "\""))
        final_data = self.client().get(
            '/bucketlists/{}'.format(json_data['id']))
        self.assertEqual(final_data.status_code, 200)
        self.assertIn('Climb the Himalayas', str(final_data.data))

    def test_edit_bucketlist(self):
        """a method to test the editing of a bucket list"""
        result_of_post_method = self.client().post(
            '/bucketlists/',
            data={'name': 'Summer, Winter'})
        self.assertEqual(result_of_post_method.status_code, 201)
        result_of_put_method = self.client().put(
            '/bucketlists/1',
            data={
                "name": "The seasons will be, summer winter and autumn"
            })
        self.assertEqual(result_of_put_method.status_code, 200)
        result_of_get_method = self.client().get('/bucketlists/1')
        self.assertIn('The seasons will b', str(result_of_get_method.data))

    def test_delete_bucketlist(self):
        """a method to test the deleting of a bucket list"""
        result_of_post_method = self.client().post(
            '/bucketlists/',
            data={'name': 'Summer , Winter'})
        self.assertEqual(result_of_post_method.status_code, 201)
        result_of_delete_method = self.client().delete('/bucketlists/1')
        self.assertEqual(result_of_delete_method.status_code, 200)
        response_after_removal = self.client().get('/bucketlists/1')
        self.assertEqual(response_after_removal.status_code, 404)

    def tearDown(self):
        '''removing all set variables and deleting our database'''
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
