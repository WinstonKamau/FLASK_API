'''A module that instantiates an app and harbors routes for bucketlists
and activities'''
from flask import request
from flask import jsonify
from flask import abort
from flask import make_response
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_configurations
db = SQLAlchemy()
#The import below has to appear after initialisation of db to SQLAlchemy
#This is because the the extensions uses the db
from .extensions import registration_login_blueprint


def create_app(config_name):
    '''A method that initialises an instance of an app with attributes'''
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
        a bucketlist if GET is chosen, the buckest list returned can be
        thinned down by an id'''
        header = request.headers.get('Authorization')
        if not header:
            response = jsonify({
                'message': 'No authorisation header given'
            })
            return make_response(response), 401
        if ' ' not in header:
            response = jsonify({
                'message1': 'A space needs to exist between the Bearer and token.',
                'message2': 'The authorization should be typed as the example below',
                'example': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1'
                           'MDMzNDUzMjIsInN1YiI6MiwiaWF0IjoxNTAzMzQxNzIyfQ.fCZ3ibX-vH'
                           'Q5SKxYbrarQ0I8lvq5TgMt03A5vGlGhDE'
            })
            return make_response(response), 401
        user_id = User.decode_token_to_sub(header)
        if not isinstance(user_id, int):
            response = {
                'message': 'User id returned is not an int',
                'userid': user_id
            }
            return make_response(jsonify(response)), 401

        if request.method == "POST":
            if 'name' not in request.data.keys():
                response = jsonify({
                    'message': 'The key variable name has not been entered!'
                })
                return make_response(response), 400
            name = str(request.data.get('name', ''))
            status_of_similarity = False
            bucketlists_to_be_checked = BucketList.query.filter_by(creator_id=user_id)
            for item in bucketlists_to_be_checked:
                if name.lower() == item.name.lower():
                    status_of_similarity = True
            if not status_of_similarity:
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
            response = jsonify({
                'message': 'A bucket list exists with a similar name of {}!'.format(name)
            })
            return make_response(response), 409
        else:
            bucket_name_to_search = request.args.get('q')
            limit_to_return = request.args.get('limit')
            no_argument_given = request.args
            if bucket_name_to_search == '':
                response = jsonify({
                    'message': 'The search parameter has no string in it'
                })
                return make_response(response), 400
            elif bucket_name_to_search:
                bucketlist_list = BucketList.query.filter_by(creator_id=user_id)
                buckets = []
                for item in bucketlist_list:
                    if bucket_name_to_search.lower() in item.name.lower():
                        a_bucket_object = {
                            'id': item.id,
                            'name': item.name,
                            'date_created': item.date_created,
                            'date_modified': item.date_modified,
                            'creator_id': item.creator_id
                            }
                        buckets.append(a_bucket_object)
                if len(buckets) > 0:
                    response = jsonify(buckets)
                    return make_response(response), 200
                response = jsonify({
                    'message': 'Name does not exist',
                })
                return make_response(response), 200
            elif limit_to_return:
                if int(limit_to_return) > 0:
                    bucketlist_list = BucketList.query.filter_by(creator_id=user_id).limit(int(limit_to_return))
                    buckets = []
                    for item in bucketlist_list:
                        a_bucket_object = {
                            'id': item.id,
                            'name': item.name,
                            'date_created': item.date_created,
                            'date_modified': item.date_modified,
                            'creator_id': item.creator_id
                        }
                        buckets.append(a_bucket_object)
                    response = jsonify(buckets)
                    return make_response(response), 200
                elif int(limit_to_return) == 0:
                    response = jsonify({
                        'message': 'Zero returns no buckets'
                    })
                    return make_response(response), 200
                response = jsonify({
                    'message': 'The value entered on limit is not suitable'
                })
                return make_response(response), 400
            elif len(no_argument_given) == 0:
                list_of_bucketlist = BucketList.query.filter_by(creator_id=user_id)
                bucketlist_objects_list = []
                for item in list_of_bucketlist:
                    a_bucket_object = {
                        'id': item.id,
                        'name': item.name,
                        'date_created': item.date_created,
                        'date_modified': item.date_modified,
                        'creator_id': item.creator_id,
                    }
                    bucketlist_objects_list.append(a_bucket_object)
                #converting the bucket list objec into JSON
                response = jsonify(bucketlist_objects_list)
                return make_response(response), 200
            response = jsonify({
                'message': 'Wrong route given. Below are the right routes',
                'GET all bucketlists for user': '/bucketlists/',
                'search particular bucketlist': '/bucketlists/?q=<name of bucket>',                    'enter a limt to bucket list returned': 'bucketlsits/?limit=<integer>'
            })
            return make_response(response), 400
    @app.route('/bucketlists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def bucketlist_manipulation(id, **kwargs):
        '''a method that accepts a variable on its route and converts it into an integer
        which is used in setting it as an id. The id allows editing and deleting a
        particular object
        '''
        header = request.headers.get('Authorization')
        if not header:
            response = jsonify({
                'message': 'No authorisation header given'
            })
            return make_response(response), 401
        if ' ' not in header:
            response = jsonify({
                'message1': 'A space needs to exist between the Bearer and token.',
                'message2': 'The authorization should be typed as the example below',
                'example': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1M'
                           'DMzNDUzMjIsInN1YiI6MiwiaWF0IjoxNTAzMzQxNzIyfQ.fCZ3ibX-vHQ5'
                           'SKxYbrarQ0I8lvq5TgMt03A5vGlGhDE"'
            })
            return make_response(response), 401
        user_id = User.decode_token_to_sub(header)
        if not isinstance(user_id, int):
            response = {
                'message': 'User id returned is not an int',
                'userid': user_id
            }
            return make_response(jsonify(response)), 401
        bucket_object = BucketList.query.filter_by(id=id, creator_id=user_id).first()
        if not bucket_object:
            return {
                'message':'The id {} entered does not exist in the bucketlist'.format(id)
            }, 400

        if request.method == 'DELETE':
            bucket_object.delete_bucket()
            return {
                "message": "bucketlist {} deleted successfully".format(bucket_object.id)
            }, 200

        elif request.method == 'PUT':
            name = str(request.data.get('name', ''))
            status_of_similarity = False
            if not name:
                response = jsonify({
                    'message': 'The key variable name has not been entered!'
                })
                return make_response(response), 400
            else:
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
                    return make_response(response), 201
                else:
                    response = jsonify({
                        'message': 'A bucket list exists with a similar name of {}!'.format(name)
                    })
                    return make_response(response), 409
        response = jsonify({
            'id': bucket_object.id,
            'name': bucket_object.name,
            'date_created': bucket_object.date_created,
            'date_modified': bucket_object.date_modified,
            'creator_id': bucket_object.creator_id
        })
        return make_response(response), 200


    @app.route('/bucketlists/<int:bucket_id>/items/', methods=['POST', 'GET'])
    def activities(bucket_id):
        header = request.headers.get('Authorization')
        if not header:
            response = jsonify({
                'message': 'No authorisation header given'
            })
            return make_response(response), 401
        if ' ' not in header:
            response = jsonify({
                'message1': 'A space needs to exist between the Bearer and token.',
                'message2': 'The authorization should be typed as the example below',
                'example': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1M'
                           'DMzNDUzMjIsInN1YiI6MiwiaWF0IjoxNTAzMzQxNzIyfQ.fCZ3ibX-vHQ5S'
                           'KxYbrarQ0I8lvq5TgMt03A5vGlGhDE"'
            })
            return make_response(response), 401
        user_id = User.decode_token_to_sub(header)
        if not isinstance(user_id, int):
            response = {
                'message': 'User id returned is not an int',
                'userid': user_id
            }
            return make_response(jsonify(response)), 401
        if not BucketList.query.filter_by(creator_id=user_id, id=bucket_id).first():
            response = {
                'message': 'The bucket id {} entered does not exist for this user'.format(bucket_id)
            }
            return make_response(response), 400
        if request.method == 'POST':
            activity_name = str(request.data.get('activity_name', ''))
            if not activity_name:
                response = jsonify({
                    'message': 'The activity_name key has not been entered therefore the activity'
                               ' has not been created'
                })
                return make_response(response), 400
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
                return make_response(response), 409
        else:
            search = request.args.get('q')
            limit_to_return = request.args.get('limit')
            no_argument_given = request.args
            if search == '':
                response = jsonify({
                    'message': 'The search parameter has no string in it'
                })
                return make_response(response), 400
            elif search:
                activities_list = Activities.query.filter_by(bucket_id=bucket_id)
                activity_array = []
                for item in activities_list:
                    if search.lower() in item.activity_name.lower():
                        activity_object = {
                            'id': item.id,
                            'activity_name': item.activity_name,
                            'date_created': item.date_created,
                            'date_modified': item.date_modified,
                            'bucket_id': item.bucket_id
                            }
                        activity_array.append(activity_object)
                if len(activity_array) > 0:
                    response = jsonify(activity_array)
                    return make_response(response), 200
                else:
                    response = jsonify({
                        'message': 'The activity name does not exist'
                    })
                    return make_response(response), 200
            elif limit_to_return:
                if int(limit_to_return) > 0:
                    activities_list = Activities.query.filter_by(bucket_id=bucket_id).limit(int(limit_to_return))
                    activity_array = []
                    for item in activities_list:
                        activity_object = {
                            'id': item.id,
                            'activity_name': item.activity_name,
                            'date_created': item.date_created,
                            'date_modified': item.date_modified,
                            'bucket_id': item.bucket_id
                        }
                        activity_array.append(activity_object)
                    response = jsonify(activity_array)
                    return make_response(response), 200
                else:
                    response = jsonify({
                        'message': 'Zero returns no item'
                    })
                    return make_response(response), 200
            elif len(no_argument_given) == 0:
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
                response = jsonify({
                    'message': 'Wrong route given. Below are the right routes',
                    'GET all items for user': '/bucketlists/<bucket_id>/items/',
                    'search particular item': '/bucketlists/<bucket_id>/items/?q=<name of bucket>',
                    'enter a limt to items returned': 'bucketlsits/<bucket_id>/items/?limit=<integer>'
                })
                return make_response(response), 400

    @app.route('/bucketlists/<int:bucket_id>/items/<int:activity_id>', methods=['GET', 'PUT', 'DELETE'])
    def activity_manipulation(bucket_id, activity_id):
        header = request.headers.get('Authorization')
        if not header:
            response = jsonify({
                'message': 'No authorisation header given'
            })
            return make_response(response), 401
        if ' ' not in header:
            response = jsonify({
                'message1': 'A space needs to exist between the Bearer and token.',
                'message2': 'The authorization should be typed as the example below',
                'example': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MDMzNDUzMjIsInN1YiI6MiwiaWF0IjoxNTAzMzQxNzIyfQ.fCZ3ibX-vHQ5SKxYbrarQ0I8lvq5TgMt03A5vGlGhDE"'
            })
            return make_response(response), 401
        user_id = User.decode_token_to_sub(header)
        if not isinstance(user_id, int):
            response = {
                'message': 'User id returned is not an int',
                'userid': user_id
            }
            return make_response(jsonify(response)), 401
        if not BucketList.query.filter_by(creator_id=user_id, id=bucket_id).first():
            response = {
                'message': 'The bucket id {} entered does not exist for this user'.format(bucket_id)
            }
            return make_response(response), 400
        activity_object = Activities.query.filter_by(bucket_id=bucket_id, id=activity_id).first()
        if not activity_object:
            response = {
                'message': 'The actvitiy id {} entered does not exist for this user'.format(activity_id)
            }
            return make_response(response), 400
        if request.method == 'PUT':
            activity_name = request.data['activity_name']
            if not activity_name:
                response = jsonify({
                    'message': 'No key of activity_name was used in replacing'
                })
                return make_respons(response), 400
            activities_to_be_checked = Activities.query.filter_by(bucket_id=bucket_id)
            status_of_similarity = False
            for item in activities_to_be_checked:
                if activity_name.lower() == item.activity_name.lower():
                    status_of_similarity = True
            if status_of_similarity == False:
                activity_object.activity_name = activity_name
                activity_object.save_activity()
                response = jsonify({
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
                return make_response(response), 409
        if request.method == 'DELETE':
            response = jsonify({
                'message': "Deleted activity {}".format(activity_object.id)
            })
            activity_object.delete_activity()
            return make_response(response), 200
        else:
            response = jsonify({
                'id': activity_object.id,
                'date_created': activity_object.date_created,
                'date_modified': activity_object.date_modified,
                'bucket_id': activity_object.bucket_id,
                'activity_name': activity_object.activity_name
            })
            return make_response(response), 200
    app.register_blueprint(registration_login_blueprint)
    return app
