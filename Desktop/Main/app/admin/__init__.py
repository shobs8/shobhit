from flask import Blueprint, request, redirect, url_for, current_app
from pymongo import MongoClient
from flask_login import current_user
import functools
from .config import Config

admin_bp = Blueprint('admin', __name__, template_folder='templates')

client = MongoClient('mongodb://localhost:27017/')
db = client.main_app





from . import routes
