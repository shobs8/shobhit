from flask import Flask, redirect, url_for, request
from flask_socketio import SocketIO
from flask_login import LoginManager
from .api.routes import api, db
from .admin.routes import admin_bp
from .api.data import User
from .admin.data import Admin
from .api.cache import cache
from .api.scheduler import sched


def create_app(debug=False):
    app = Flask(__name__, static_url_path='/static')
    app.debug = debug
    app.config['SECRET_KEY'] = 'secret'
    # app.config.from_pyfile('settings.cfg')

    app.config['CACHE_TYPE']="redis"
    app.config['CACHE_REDIS_HOST']="localhost"
    app.config['CACHE_REDIS_PORT']="6379"
    app.config['CACHE_REDIS_PASSWORD']= "TTLnnqTy9di5m6IPmwxq8z/Bgpm3XkuSYJyBxrFcbcEe8kFr8O78TH39nhJEUHzJ9QuIKSAEh6jNMaAb"
    app.config['CACHE_REDIS_DB']="0"
    # ##################################################################

    cache.init_app(app)

    # Start the Scheduler
    sched.start()

    # login
    login = LoginManager(app)
    login.login_view = 'api.login'
    login.init_app(app)

    # load user
    @login.user_loader
    def load_user(username):

        current_user = None
        if request.blueprint == 'admin':
            admin = db.Admins.find_one({'id': username})
            if admin:
                current_user = Admin(admin['id'])
        elif request.blueprint == 'api':
            user = db.Users.find_one({'id':username})
            if user:
                current_user = User(user['id'], user['email']) 

        return current_user


    # Unauthorized Handler
    @login.unauthorized_handler
    def unauth_handler():
        # if request url is api, redirect to api.login
        if request.blueprint == 'api':
            return redirect(url_for('api.login'))
        # if request url is admin, redirect to admin.login
        elif request.blueprint == 'admin':
            return redirect(url_for('admin.login'))
        

    # API Blueprint
    app.register_blueprint(api)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Chat
    socketio = SocketIO()
    socketio.init_app(app)

    # Add Scheduler Method
    # sched.add_job(func=db_to_cache, trigger="interval", seconds=10)
    return app