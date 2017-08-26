'''A module that contains documentation for swagger implementation
which maps to the files for the flask api
'''
import os
from flasgger import Swagger

from app import create_app

CONFIG_NAME = os.getenv('APP_SETTINGS')
app = create_app(CONFIG_NAME)
SWAGGER = Swagger(app)

@app.route('/auth/register', methods=['POST'])
def register_user():
    """Endpoint creating a user
    To register insert a valid email address such as 'don.joe@gmail.com' or 'donito@gmail.com'
    Insert a password for the email that you insert. The password can be a string.
    ---
    parameters:
      - name: user_email
        in: formData
        type: string
        description: A valid email for a user
        required: true
      - name: user_password
        in: formData
        type: string
        description: password for the user
        required: true
    responses:
      201:
        description: User has been created
      401:
        description: User creation has been unauthorised by the server
      409:
        description: An identical user with the same email address already exists.
      400:
        description: Key variables used or the values entered are not suitable. Bad request.
   """
    pass

@app.route('/auth/login', methods=['POST'])
def login_user():
    """Endpoint logging in a user
    To login ensure that you have an account that is registered. Insert a valid email address
    on the key variable user_email and the password registered it with.
    ---
    parameters:
      - name: user_email
        in: formData
        type: string
        description: A valid email for a user
        required: true
      - name: user_password
        in: formData
        type: string
        description: password for the user
        required: true
    responses:
      400:
        description: Key variables to be entered are supposed
          to be user_email and user_password. The email has to be valid.
      401:
        description: User has been unauthorised.
      200:
        description: User has been logged in.
    """
    pass

@app.route('/auth/reset-password', methods=['POST'])
def reset_password():
    """Endpoint reseting password for a user
    Insert the current password that you use for your account on the user_password key.
    Insert a new password for your account on the new_password key.
    Verify that you inserted it right by inserting it on the verify_new_password key.
    ---
    parameters:
      - name: user_password
        in: formData
        type: string
        description: Current password for the user
        required: true
      - name: new_password
        in: formData
        type: string
        description: New password for the user
        required: true
      - name: verify_new_password
        in: formData
        type: string
        description: Password verifier for the user
        required: true
    responses:
      401:
       description: Unauthorised.
      400:
        description: The request made has an error witht the data given.
      201:
        description: New password generated.
    """
    pass

@app.route('/auth/logout', methods=['POST'])
def logout_user():
    """Endpoint logging out a user
    Log out the user by pressing the button
    ---
    responses:
      200:
        description: User logged out
    """
    pass

@app.route('/bucketlists/', methods=['POST'])
def post_bucketlist():
    """Endpoint for posting a bucketlist
    On the variable name insert a name for the bucket list
    ---
    parameters:
      - name: name
        in: formData
        type: string
        description: A bucket name that does not exist in the bucketlist
        required: true
      - name: Authorization
        description: Token that should begin with the word Beare and a space 'Bearer '
        in: header
        type: string
        required: true
    responses:
      401:
        description: Unauthorised
      400:
        description: No bucket name entered
      201:
        description: Bucket name created
      409:
        description: The bucket name entered already exists in the bucketlist
    """
    pass

@app.route('/bucketlists/')
def get_bucketlist():
    """Endpoint for getting a bucketlist
    A route that returns all the bucketlists for the user if no arguments are provided.
    Authorization refers to the clients token for authorising a user.
    Q asks for a string on th bucket name to enter.
    Limit asks for an integer to limit the number of buckets to return
    ---
    parameters:
      - name: Authorization
        description: Token that should begin with the word Bearer and a space after to
           separate the two statements 'Bearer '
        in: header
        type: string
        required: true
      - name: q
        description: A query for asking for the string for searching
        in: query
        type: string
      - name: limit
        description: A limit for returning the number of buckets inserted
        in: query
        type: integer
    responses:
      200:
        description: Request passed
      400:
        description: Wrong value entered on the limit or bad route
      401:
        description: User unauthorized
    """
    pass

@app.route('/bucketlists/<int:id>', methods=['GET'])
def manipulate_bucketlist():
    """Endpoint for getting a specific bucket using its id
    Insert integer for the id to get the bucket list using its bucket id.
    Authorization refers to the client's token for authorising a user.
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The bucket list id
      - name: Authorization
        description: Token that should begin with the word Bearer and a space after
           to separate the two statements 'Bearer token'
        in: header
        type: string
        required: true
    responses:
      401:
        description: User unauthorized due to wrong id for the bucket list
      400:
        description: The id does not represent an id for a bucket in the bucketlist
      200:
        description: The bucket item with the bucket id above has been returned
    """
    pass

@app.route('/bucketlists/<id>', methods=['PUT'])
def update_bucketlist():
    """Endpoint for updating a bucketlist
    The route updates a bucket using the id of the bucket to determine the exact
    bucket and a name to replace the original name of the bucket
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: An id for the bucket.
      - name: name
        in: formData
        type: string
        description: A bucket name that does not already exist in the user's bucketlist.
        required: true
      - name: Authorization
        description: Token that should begin with the word Bearer and a space after to
           separate the two statements 'Bearer token'
        in: header
        type: string
        required: true
    responses:
      401:
        description: User has not been authorized majorly due to wrong token supplied
      400:
        description: Bad request due to wrong id or no name granted for the bucket
      201:
        description: Bucket replaced and new bucket created
      409:
        description: A similar bucket with the same name was created before
    """
    pass

@app.route('/bucketlists/<int:id>', methods=['DELETE'])
def delete_bucketlist():
    """Endpoint for deleting a bucketlist
    The route deletes a bucket using the id supplied by the user
    ---
    parameters:
    - name: Authorization
      description: Token that should begin with the word Bearer and a space after to
        separate the two statements 'Bearer token'
      in: header
      type: string
      required: true
    - name: id
      in: path
      type: integer
      required: true
      description: An id for the bucket.
    responses:
      401:
        description: User has not been authorized majorly due to wrong token supplied
      400:
        description: Bad request due to wrong id granted for the bucket
      200:
        description: Bucket has been deleted
    """
    pass

@app.route('/bucketlists/<int:bucket_id>/items/', methods=['POST'])
def post_activities():
    """Endpoint for deleting an activity
    Post an activity on a particular bucket by using the bucket id
    ---
    parameters:
      - name: activity_name
        in: formData
        type: string
        description: An activity within the bucketlist, that does not exist in the
          specific bucketlist
        required: true
      - name: bucket_id
        in: path
        type: integer
        description: The id for the bucket
        required: true
      - name: Authorization
        description: Token that should begin with the word Bearer and a space after
           to separate the two statements 'Bearer token'
        in: header
        type: string
        required: true
    responses:
      401:
        description: User has not been authorized majorly due to wrong token supplied
      400:
        description: Bad request due to id or no activity name supplied
      201:
        description: New activity name created
      409:
        description: Activity not created because it already exists in this users
           bucket list as it was created before
    """
    pass

@app.route('/bucketlists/<int:bucket_id>/items/', methods=['GET'])
def get_activities():
    """Endpoint for getting activities
    A method for returning activities, by supplying an id for a specific bucket
    ---
    parameters:
      - name: bucket_id
        in: path
        type: integer
        description: The id for the bucket
        required: true
      - name: Authorization
        description: Token that should begin with the word Bearer and a space
           after to separate the two statements 'Bearer token'
        in: header
        type: string
        required: true
    responses:
      401:
        description: Users unauthorized
      400:
        description: Bad reqeust possibly because wrong id supplied for the
           bucket list, no data given for search parameter
      200:
        description: Request acted on
    """
    pass

@app.route('/bucketlists/<int:bucket_id>/items/<int:activity_id>', methods=['GET'])
def manipulate_activity():
    """Endpoint for retrieving a particular activity
    A route for returning a specific activity using its bucket_id and activity_id
    ---
    parameters:
      - name: activity_id
        in: path
        required: true
        description: An id for an activity the user wants to retrieve
        type: integer
      - name: bucket_id
        in: path
        required: true
        description: An id for a bucket a user wants to retrieve an activity from
        type: integer
      - name: Authorization
        description: Token that should begin with the word Bearer and a space
           after to separate the two statements 'Bearer token'
        in: header
        type: string
        required: true
    responses:
      401:
        description: Unauthorized
      400:
        description: Bad request, bucket id does not exist for this user,
           activity id does not exist for this user
      200:
        description: Activity returned successfully
    """
    pass

@app.route('/bucketlists/<int:bucket_id>/items/<int:activity_id>', methods=['PUT'])
def update_activity():
    """Endpoint for updating an activity
    A method for updating an activity by replacing the name of the activity
    ---
    parameters:
      - name: activity_name
        in: formData
        type: string
        description: An activity within the bucketlist, that does not exist in the
           specific bucketlist
        required: true
      - name: activity_id
        in: path
        required: true
        description: An id for an activity the user wants to retrieve
        type: integer
      - name: bucket_id
        in: path
        required: true
        description: An id for a bucket a user wants to retrieve an activity from
        type: integer
      - name: Authorization
        description: Token that should begin with the word Bearer and a space after
           to separate the two statements 'Bearer token'
        in: header
        type: string
        required: true
    responses:
      401:
        description: User unauthorized
      400:
        description: Bad request the bucket does not exist or the activity does not
           exist from the respective ids given by the user
      409:
        description: Activity name had been entered before posing conflict with new
           activity name inserted
      200:
        description: Activity updated
    """
    pass

@app.route('/bucketlists/<int:bucket_id>/items/<int:activity_id>', methods=['DELETE'])
def delete_activity():
    """Endpoint for deleting an activity
    A method for deleting an activity using the bucket and activity id
    ---
    parameters:
      - name: activity_id
        in: path
        required: true
        description: An id for an activity the user wants to retrieve
        type: integer
      - name: bucket_id
        in: path
        required: true
        description: An id for a bucket a user wants to retrieve an activity from
        type: integer
      - name: Authorization
        description: Token that should begin with the word Bearer and a space
           after to separate the two statements 'Bearer token'
        in: header
        type: string
        required: true
    responses:
      401:
        description: Unauthorized
      400:
        description: Bad request the bucket id and activity id does not exist
      200:
        description: Activity id deleted
    """
    pass

app.run(debug=True)
