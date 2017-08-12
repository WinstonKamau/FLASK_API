'''A module to test the Bucket List class on crud for activities in a
bucketlit
'''
import unittest
import os
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

        with self.app.app_context():
            db.create_all()
    
    def test_activity_creation(self):
        """A method to test that the API creates an activity"""
        result_of_post_bucket = self.client().post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(result_of_post_bucket.status_code, 201)
        result_of_post_activity = self.client().post('/bucketlists/1/items/', data=self.activity)
        self.assertIn('Climb the Himalayas', str(result_of_post_activity.data))