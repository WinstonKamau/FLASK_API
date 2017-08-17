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
                if name:
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
                list_of_bucketlist = BucketList.query.filter_by(creator_id=user_id)
                bucketlist_objects_list = []

                for item in list_of_bucketlist:
                    a_bucket_object = {
                                        'id': item.id,
                                        'name': item.name,
                                        'date_created': item.date_created,
                                        'date_modified': item.date_modified,
                                        'creator_id': user_id
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
        
    app.register_blueprint(registration_login_blueprint)
    return app
