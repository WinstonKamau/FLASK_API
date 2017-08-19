from flask import request
from flask import jsonify
from flask import abort
from flask import make_response
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_configurations
db=SQLAlchemy()
#The import below has to appear after initialisation of db to SQLAlchemy
#This is because the the extensions uses the db
from .extensions import registration_login_blueprint



def create_app(config_name):
    from app.models import User
    from app.models import BucketList
    from app.models import Activities
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_configurations[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    @app.route('/bucketlists/', methods=['POST', 'GET'])
    def bucketlists():
        '''a method that will save a bucket list if post is chosen, return
        a bucketlist if GET is chosen, the bucket list returned can be
        thinned down by an id'''
        header = request.headers.get('Authorization')
        splitted_header = header.split(' ')
        token = splitted_header[1]
        user_id = User.decode_token_to_sub(token)
        if not isinstance(user_id, str):
            if request.method == "POST":
                name = str(request.data.get('name', ''))
                status_of_similarity = False
                if name:
                    bucketlists_to_be_checked = BucketList.query.filter_by(creator_id=user_id)
                    for item in bucketlists_to_be_checked:
                        if name.lower() == item.name.lower():
                            status_of_similarity = True     
                    if status_of_similarity == False:
                        bucket_object = BucketList(name=name, creator_id=user_id)
                        bucket_object.save_bucket()
                        response = jsonify({
                            'id': bucket_object.id,
                            'name': bucket_object.name,
                            'date_created': bucket_object.date_created,
                            'date_modified': bucket_object.date_modified,
                            'creator_id': user_id
                        })
                        return make_response(response), 201
                    else:
                        response = jsonify ({
                            'message': 'A bucket list exists with a similar name of {}!'.format(name)
                        })
                        return make_response(response), 202
                else:
                    response = jsonify ({
                        'message': 'The key variable name has not been entered!'
                    })
                    return make_response(response), 400
            else:
                bucket_name_to_search = request.args.get('q')
                if bucket_name_to_search:
                    bucketlist_list = BucketList.query.filter_by(creator_id = user_id) 
                    buckets = []
                    for item in bucketlist_list:
                        if item.name == bucket_name_to_search:
                            a_bucket_object = {
                                            'id': item.id,
                                            'name': item.name,
                                            'date_created': item.date_created,
                                            'date_modified': item.date_modified,
                                            'creator_id': item.creator_id
                                        }
                            buckets.append(a_bucket_object)
                    if len(buckets) > 0 :
                        response = jsonify (buckets)    
                        return make_response(response), 200
                    else:
                        response = jsonify({
                            'message': 'Name does not exist'
                        })
                        return make_response(response), 202
                else: 
                    list_of_bucketlist = BucketList.query.filter_by(creator_id=user_id)
                    bucketlist_objects_list = []

                    for item in list_of_bucketlist:
                        a_bucket_object = {
                                            'id': item.id,
                                            'name': item.name,
                                            'date_created': item.date_created,
                                            'date_modified': item.date_modified,
                                            'creator_id': item.creator_id
                        }
                        bucketlist_objects_list.append(a_bucket_object)
                    #converting the bucket list objec into JSON
                    response = jsonify(bucketlist_objects_list)
                    return make_response(response), 200
        else:
            response = {
                'message': 'User id is a string',
                'userid': user_id
            }
            return make_response(jsonify(response)), 401

    @app.route('/bucketlists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def bucketlist_manipulation(id, **kwargs):
        '''a method that accepts a variable on its route and converts it into an integer
        which is used in setting it as an id. The id allows editing and deleting a
        particular object
        '''
        header = request.headers.get('Authorization')
        splitted_header = header.split(' ')
        token = splitted_header[1]
        user_id = User.decode_token_to_sub(token)
        if not isinstance(user_id, str):
            bucket_object = BucketList.query.filter_by(id=id).first()
            if not bucket_object:
                abort(404)

            if request.method == 'DELETE':
                bucket_object.delete_bucket()
                return {
                "message": "bucketlist {} deleted successfully".format(bucket_object.id) 
            }, 200

            elif request.method == 'PUT':
                name = str(request.data.get('name', ''))
                status_of_similarity = False
                if name:
                    bucketlists_to_be_checked = BucketList.query.filter_by(creator_id=user_id)
                    for item in bucketlists_to_be_checked:
                        if name.lower() == item.name.lower():
                            status_of_similarity = True     
                    if status_of_similarity == False:
                        bucket_object.name = name
                        bucket_object.save_bucket()
                        response = jsonify({
                            'id': bucket_object.id,
                            'name': bucket_object.name,
                            'date_created': bucket_object.date_created,
                            'date_modified': bucket_object.date_modified,
                            'creator_id': bucket_object.creator_id
                        })
                        return make_response(response), 200
                    else:
                        response = jsonify ({
                            'message': 'A bucket list exists with a similar name of {}!'.format(name)
                        })
                        return make_response(response), 202
                else:
                    response = jsonify ({
                        'message': 'The key variable name has not been entered!'
                    })
                    return make_response(response), 400
            else:
                response = jsonify({
                    'id': bucket_object.id,
                    'name': bucket_object.name,
                    'date_created': bucket_object.date_created,
                    'date_modified': bucket_object.date_modified,
                    'creator_id': bucket_object.creator_id
                })
                return make_response(response), 200
        else:
            response = {
                'message': 'User id is a string',
                'userid': user_id
            }
            return make_response(jsonify(response)), 401
    @app.route('/bucketlists/<int:bucket_id>/items/', methods=['POST', 'GET'])
    def activities(bucket_id):
        header = request.headers.get('Authorization')
        splitted_header = header.split(" ")
        token = splitted_header[1]
        user_id = User.decode_token_to_sub(token)
        if not isinstance(user_id, str):
            if request.method == 'POST':
                activity_name = str(request.data.get('activity_name', ''))
                if activity_name:
                    activities_to_be_checked = Activities.query.filter_by(bucket_id=bucket_id)
                    status_of_similarity = False
                    for item in activities_to_be_checked:
                        if activity_name.lower() == item.activity_name.lower():
                            status_of_similarity = True
                    if status_of_similarity == False:
                        activity_object = Activities(activity_name=activity_name, bucket_id=bucket_id)    
                        activity_object.save_activity()
                        response = jsonify({
                            'id': activity_object.id,
                            'activity_name': activity_object.activity_name,
                            'date_created': activity_object.date_created,
                            'date_modified': activity_object.date_modified,
                            'bucket_id': activity_object.bucket_id
                        })
                        return make_response(response), 201
                    else:
                        response = jsonify({
                            'message': "An activity already exists with the name {} provided.".format(activity_name)
                        })
                        return make_response(response), 202
                else:
                    response = jsonify ({
                        'message': 'The activity_name key has not been entered therefore the activity has not been created',
                    })
                    return make_response(response), 400
            else:
                activitieslist = Activities.query.filter_by(bucket_id=bucket_id)
                activity_array = []
                for item in activitieslist:
                    activity_item = {
                        'id': item.id,
                        'activity_name': item.activity_name,
                        'date_created': item.date_created,
                        'date_modified': item.date_modified,
                        'bucket_id': item.bucket_id 
                    }
                    activity_array.append(activity_item)
                response = jsonify(activity_array)
                return make_response(response), 200
        else:
            response = {
                'message': 'User is is a string',
                'userid': user_id
            }
            return make_response(jsonify(response)), 401
    @app.route('/bucketlists/<int:bucket_id>/items/<int:activity_id>', methods = ['GET', 'PUT', 'DELETE'])
    def activity_manipulation(bucket_id, activity_id):
        header = request.headers.get('Authorization')
        splitted_header = header.split(" ")
        token = splitted_header[1]
        user_id = User.decode_token_to_sub(token)
        if not isinstance(user_id, str):
            activity_object = Activities.query.filter_by(id=activity_id).first()
            if not activity_object:
                abort (404)
            if request.method == 'PUT':
                activity_name = request.data['activity_name']
                if activity_name:
                    activities_to_be_checked = Activities.query.filter_by(bucket_id=bucket_id)
                    status_of_similarity = False
                    for item in activities_to_be_checked:
                        if activity_name.lower() == item.activity_name.lower():
                            status_of_similarity = True
                    if status_of_similarity == False:
                        activity_object.activity_name = activity_name
                        activity_object.save_activity()
                        response = jsonify ({
                            'id': activity_object.id,
                            'date_created': activity_object.date_created,
                            'date_modified': activity_object.date_modified,
                            'bucket_id': activity_object.bucket_id,
                            'activity_name': activity_object.activity_name
                        })
                        return make_response(response), 200
                    else:
                        response = jsonify({
                            'message': "An activity already exists with the name {} provided.".format(activity_name)
                        })
                        return make_response(response), 202
                else:
                    response = jsonify({
                        'message': 'No key of activity_name was used in replacing'
                    }) 
                    return make_respons(response), 400
            if request.method == 'DELETE':
                response = jsonify({
                    'message': "Deleted activity {}".format(activity_object.id)
                })
                activity_object.delete_activity()
                return make_response(response), 200 
               
            else:
                response = jsonify ({
                    'id': activity_object.id,
                    'date_created': activity_object.date_created,
                    'date_modified': activity_object.date_modified,
                    'bucket_id': activity_object.bucket_id,
                    'activity_name': activity_object.activity_name
                })    
                return make_response(response), 200
        else:
            response = {
                'message': 'The user id is a string and not an integer',
                'user_id': user_id
            }
    
    
    
    app.register_blueprint(registration_login_blueprint)
    return app
