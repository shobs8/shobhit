from flask import current_app
from flask_login import current_user
import functools

def permission_required(perms_list):
    def wrapper(fn):
        @functools.wraps(fn)
        def decorated_view(*args, **kwargs):

            if not current_user.is_authenticated:
               return current_app.login_manager.unauthorized()

            perm = current_user.has_perm()

            if not perm or perm not in perms_list:
                return current_app.login_manager.unauthorized()

            if perm in perms_list:
                return fn(*args, **kwargs)

        return decorated_view
    return wrapper

