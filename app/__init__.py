"""server api setup"""
import os
import json
import datetime
from bson.objectid import ObjectId
from flask import Flask
from flask_pymongo import PyMongo
from configparser import ConfigParser
from flask_cors import CORS

class JSONEncoder(json.JSONEncoder):
    ''' extend json-encoder class'''

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


# create the flask object
app = Flask(__name__)
CORS(app)

# Database config
app.config['MONGO_DBNAME'] = 'test'
if not os.environ.get("DB"):
    config = ConfigParser()
    config.read('setting.ini')
    app.config['MONGO_URI'] = config['DEFAULT']['DB']
else:
    app.config['MONGO_URI'] = os.environ.get("DB")

mongo = PyMongo(app)

# use the modified encoder class to handle ObjectId & datetime object while jsonifying the response.
app.json_encoder = JSONEncoder

from app import routes
