[![Build Status](https://travis-ci.org/WinstonKamau/FLASK_API.svg?branch=master)](https://travis-ci.org/WinstonKamau/FLASK_API)
# FLASK_API
Flask Api is a restful api that serves clients by allowing them to create, read, update and delete buckets as well as activities within their buckets. By buckets we refer to a larger class category of things clients would love to do in their lives before they die for example 'Travelling'. By activities/items we refer to a more detail explanation of the bucket, search as 'Travel to Morrocco and visit the formula E arena'

# Features
* The flasgger view has been used to show the endpoints of what can be done on the api*
- The flask api allows users to register using a user email and a user password
- The flask api allows users to login using their respective email an passwords
- The flask api allows users to reset passwords.
- The flask api allows users to log out, the logout function simply deletes tokens on the client server but this has not yet been implemented
- The flask api allows users to create, retrieve and manipulate buckets
- The flask api allows a user to create, retrieve and manipulate activities

# Setup

Ensure that you are working in a virtual environment
Install flask,flask-sqlalchemy psycopg2 flask-migrate, FLASK_API, flask_script, flask_bycrypt
SQLALCHEMy database
