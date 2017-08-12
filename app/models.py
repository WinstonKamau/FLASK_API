import os
from app import db


class BucketList(db.Model):
    #The table for the bucketlist with the variable name __buckettable__
    __buckettable__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default = db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default = db.func.current_timestamp(), 
                              onupdate = db.func.current_timestamp())

    def __init__(self, name):
        '''Initialising the bucket list with a name'''
        self.name = name

    def save_bucket(self):
        '''A method to save the bucket'''
        db.session.add(self)
        db.session.commit()

    def delete_bucket(self):
        '''A method to delete the bucket'''
        db.session.delete(self)
        db.session.commit()
    
    @staticmethod
    def read_bucket():
        '''A method to return the bucket list in one query'''
        return BucketList.query.all()

    def __repr__(self):
        '''A method that repesents the object instance of the model whenever it queries'''
        return "Bucketlist: {}>".format(self.name)


class Activities(db.Model):
   #table for the activities with the activity name activities
    __activitylist__="activities"
    id = db.Column(db.Integer, primary_key=True)
    activity_name = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default = db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default = db.func.current_timestamp(), 
                              onupdate = db.func.current_timestamp())

    def __init__(self, activity_name):
        '''initialising the activity name'''
        self.activity_name = activity_name
    
    def save_activity(self):
        '''A method to save the activity name'''
        db.session.add(self)
        db.session.commit()
    
    def delete_activity(self):
        '''A method to delete the activity name'''
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def read_activity():
        return Activities.query.all()
    
    def __repr__(self):
        '''A method that returns an object instance of Activity whenever it queries'''
        return "Activities: {}>".format(self.name)
