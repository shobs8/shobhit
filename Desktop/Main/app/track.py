

from flask import Flask, g
from pymongo import MongoClient
from flask_track_usage import TrackUsage
from flask_track_usage.summarization import sumUrl
from flask_mongoengine import MongoEngine
from flask_track_usage.storage.mongo import MongoEngineStorage

app = Flask(__name__)

# Set the configuration items manually for the example
app.config['TRACK_USAGE_USE_FREEGEOIP'] = False
# You can use a different instance of freegeoip like so
# app.config.cgf['TRACK_USAGE_FREEGEOIP_ENDPOINT'] = 'http://extreme-ip-lookup.com/json/'
app.config['TRACK_USAGE_INCLUDE_OR_EXCLUDE_VIEWS'] = 'include'
app.config['MONGODB_SETTINGS'] ={'db':'website'}
mongo_db =MongoEngine(app)

mstore = MongoEngineStorage(hooks=[sumUrl])
# Make an instance of the extension and put two writers
t = TrackUsage(app, [mstore ])

# dbs = list(db.usageTracking.find({}))
# a= len(dbs)
# print(dbs)
# Run the application!
