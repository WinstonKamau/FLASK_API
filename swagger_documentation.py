import os
from flask import Flask, jsonify
from flasgger import Swagger

from app import create_app 

config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)
swagger = Swagger(app)

@app.route('/auth/register', methods=['POST'])
def register_user():
    """Example endpoint creating a user
    This is using docstrings for specifications.
    ---
    parameters:
      - name: email
        in: formData
        type: string
        description: user email
        required: true
      - name: password
        in: formData
        type: string
        description: user password
        required: true
   """
    pass

@app.route('/auth/login', methods=['POST'])
def login_user():
  pass

@app.route('/auth/reset-password', methods=['POST'])
def reset_password():
  pass
@app.route('/auth/logout', methods=['GET'])
def logout_user():
  pass

app.run (debug=True)