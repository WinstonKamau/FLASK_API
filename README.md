[![Build Status](https://travis-ci.org/WinstonKamau/FLASK_API.svg?branch=master)](https://travis-ci.org/WinstonKamau/FLASK_API)

[![Coverage Status](https://coveralls.io/repos/github/WinstonKamau/FLASK_API/badge.svg?branch=master)](https://coveralls.io/github/WinstonKamau/FLASK_API?branch=master)
# FLASK_API
Flask Api is a restful api that serves clients by allowing them to create, read, update and delete buckets as well as activities within their buckets. By buckets we refer to a larger class category of things clients would love to do in their lives before they die for example 'Travelling'. By activities/items we refer to a more detail explanation of the bucket, search as 'Travel to Morrocco and visit the formula E arena'

# Features
- The flask api allows users to register using a user email and a user password
- The flask api allows users to login using their respective email an passwords
- The flask api allows users to reset passwords.
- The flask api allows users to log out, the logout function simply deletes tokens on the client server but this has not yet been implemented
- The flask api allows users to create, retrieve and manipulate buckets
- The flask api allows a user to create, retrieve and manipulate activities

#Technologies used
- Python3
- Flask
- Postgresql
# Setup
-Create a folder that will host the project
-Clone https://github.com/WinstonKamau/FLASK_API.git
-Ensure that you are working in a virtual environment. `pip install virtualenv`>
-Create a .env file
-On your .env file set you database url to link to your postgresql account.
 `export DATABASE_URL="postgresql://localhost/flask_api"` if you have a password ensure that the link above delivers the username and password. e.g. `export DATABASE_URL="postgresql://username:password@localhost/flask_api"`
-On the .env file set `export FLASK_APP to run.py`
-On the .env file set `export SECRET="any string you choose"`
-On the .env file set `export APP_SETTINGS="development`
-Install the requirements on the requirements.txt file `pip install -r requirements.txt`
-Create a migrations folder by running `python migrate db init`
-Migrate the migrations by running `python migrate db migrate`
-Run `python migrate db upgrade` to persist migrations
-To run the app on flassger use `python swagger_documentations.py`
-To run the app on postman user `flask run`
-Run the app using `python run.py `

#API ENDPOINTS
================================
**ENDPOINT** | **Public Access**
---------------------------------
POST /auth/register | True
---------------------------
POST /auth/login | True
------------------------
POST /auth/reset-password |True
--------------------------------
POST /auth/logout |True
------------------------
POST /bucketlists/|False
-------------------------
GET /bucketlists/|False
------------------------
GET /bucketlists/<id> | False
-----------------------------
PUT /bucketlists/<id>| False
-----------------------------
DELETE /bucketlists/<id> | False
---------------------------------
POST /bucketlsits/<id>/items/ | False 
---------------------------------------------
PUT /bucketlists/<id>/items/<item_id>| False
---------------------------------------------
DELETE /bucketlists/<id>/items/<item_id>| False
------------------------------------------------


