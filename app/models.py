import os
from app import db


class BucketList(db.Model):
    '''The table for the bucketlist with the variable name __buckettable__'''
    __buckettable__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default = db.func.current_time.stamp())
    date_modified = db.Column(db.DateTime, default = db.func.current_time.stamp(), 
                              onupdate = db.func.current_time.stamp())

    def __init__(self, bucket_name):
        '''Initialising the bucket list with a name'''
        self.bucket_name = bucket_name

    def save_bucket(self):
        '''A method to save the bucket'''
        db.session.add(self)
        db.session.commit()

    def delete_bucket(self):
        '''A method to delete the bucket'''
        db.session.delete(self)
        db.session.commit()
    
    @staticmethod
    def get_all():
        '''A method to return the bucket list in one query'''
        return Bucketlist.querry.all

    def __repr__(self):
        '''A method that repesents the object instance of the model whenever it queries'''
        return "Bucketlist: {}>".format(self.name)
        