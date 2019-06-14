from flask import Flask, Blueprint
from pymongo import MongoClient
from flask_login import LoginManager
from flask_socketio import SocketIO

from .config import Config

api = Blueprint('api', __name__, template_folder='templates')

client = MongoClient('mongodb://localhost:27017/')
db = client.main_app

import threading
from .worker import start_worker
t_msg = threading.Thread(target=start_worker)
t_msg.start()
t_msg.join(0)

from . import routes, events
