'''A module for communicating with the database that creates tables for
users, bucketlists and activities'''
import os

from datetime import datetime, timedelta
import jwt
from flask import current_app
from flask_bcrypt import Bcrypt
from app import db



class User(db.Model):
    '''A class that creates an instance of a user , saves, deletes and
    modifies it into tables that store the data
    '''
    #table for users
    __usertable__ = 'users'
    #id for a user
    id = db.Column(db.Integer, primary_key=True)
    #nullable set to False because it is required
    #Unique is set to True as two users cannot have the same email
    user_email = db.Column(db.String(300), nullable=False, unique=True)
    user_password = db.Column(db.String(300), nullable=False)
    bucketlists = db.relationship('BucketList',
                                  order_by='BucketList.id',
                                  cascade='all, delete-orphan')

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

    @staticmethod
    def create_encoded_token(user_id):
        '''A method to create a token based on the id of the user and encode it to send
        to the clients server
        '''
        try:
            #A payload with the attribute for the subject of the user's id
            payload = {
                'exp': datetime.utcnow() +timedelta(minutes=60),
                'sub': user_id,
                'iat': datetime.utcnow()
            }
            #Creating a json web token encoded with the algorithm HMAC SHA-256 algorithm
            json_web_token = jwt.encode(payload,
                                        current_app.config.get('SECRET'),
                                        algorithm='HS256'
                                       )
            return json_web_token

        except Exception as the_exception_generated:
            #A method to return any exception raised in the try block above
            return str(the_exception_generated)

    @staticmethod
    def decode_token_to_sub(token_received):
        '''A method for decoding the token provided back to a user id
        that can be used to get information for the specific user
        '''
        try:
            splitted_header = token_received.split(' ')
            token = splitted_header[1]
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "10 minutes passed, your token has expired"
        except jwt.InvalidTokenError:
            return 'Register and login to allow valid token'

    def password_confirm(self, user_password):
        '''A method for comparing the password entered to the password already stored in hash
        format. The method returns True if the password match or False if they do not
        '''
        return Bcrypt().check_password_hash(self.user_password, user_password)


class BucketList(db.Model):
    '''A class that creates an instance of a bucket list, saves a bucketlist
    deletes a bucket list and modifies bucket list to the database
    '''
    #The table for the bucketlist with the variable name __buckettable__
    __buckettable__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    creator_id = db.Column(db.Integer, db.ForeignKey(User.id))
    activities = db.relationship('Activities',
                                 order_by='Activities.id',
                                 cascade='all, delete-orphan')

    def __init__(self, name, creator_id):
        '''Initialising the bucket list with a name and the user's id'''
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
    '''A class that creates an instance of an activity, saves an activity,
    deletes an activity in the database
    '''
    #table for the activities with the activity name activities
    __activitylist__ = "activities"

    id = db.Column(db.Integer, primary_key=True)
    activity_name = db.Column(db.String(300))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    bucket_id = db.Column(db.Integer, db.ForeignKey(BucketList.id))


    def __init__(self, activity_name, bucket_id):
        '''initialising the activity name, user's and bucketlist's id'''
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
    def read_activity(activity_id):
        '''A method that reads an activity using its id'''
        return Activities.query.all(activity_id=activity_id)

    def __repr__(self):
        '''A method that returns an object instance of Activity whenever it queries'''
        return "Activities: {}>".format(self.activity_name)
