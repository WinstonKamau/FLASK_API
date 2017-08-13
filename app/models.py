import os
from app import db
from flask_bcrypt import Bcrypt


class User(db.Model):
    #table for users
    __usertable__ = 'users'
    #id for a user
    id = db.Column(db.Integer, primary_key=True)
    #nullable set to False because it is required
    #Unique is set to True as two users cannot have the same email
    user_email = db.Column(db.String(40), nullable=False, unique=True)
    user_password = db.Column(db.String(40), nullable=False)
    bucketlists = db.relationship('BucketList', order_by='BucketList.id', cascade='all, delete-orphan')

    def __init__(self, user_email, user_password):
        '''A method for initialising the user with an email and a password that has been hashed
        inorder to prevent storing password in plain text which could be accessed through brute 
        force approaches
        '''
        self.user_email = user_email
        #the decode method is a python 3 language specific method for using utf-8
        #Calls the Bycrypt object method to generate a hashed password
        self.user_password = Bcrypt().generate_password_hash(user_password).decode()

    def save_user(self):
        '''A method for adding a user to the database'''
        db.session.add(self)
        db.session.commit()
    
    def password_confirm(self, user_password):
        '''A method for comparing the password entered to the password already stored in hash
        format. The method returns True if the password match or False if they do not
        '''
        return Bcrypt().check_password_hash(self.user_password, user_password)


class BucketList(db.Model):
    #The table for the bucketlist with the variable name __buckettable__
    __buckettable__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default = db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default = db.func.current_timestamp(), 
                              onupdate = db.func.current_timestamp())
    creator_id = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self, name, creator_id):
        '''Initialising the bucket list with a name'''
        self.name = name
        self.creator_id = creator_id

    def save_bucket(self):
        '''A method to save the bucket'''
        db.session.add(self)
        db.session.commit()

    def delete_bucket(self):
        '''A method to delete the bucket'''
        db.session.delete(self)
        db.session.commit()
    
    @staticmethod
    def read_bucket(user_id):
        '''A method to return the bucket list in one query'''
        return BucketList.query.all(creator_id=user_id)

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
    bucket_id = db.Column(db.Integer)


    def __init__(self, activity_name, bucket_id):
        '''initialising the activity name'''
        self.activity_name = activity_name
        self.bucket_id = bucket_id
    
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
