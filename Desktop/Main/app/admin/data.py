from .admin import db
from uuid import uuid4 as uid
from werkzeug.security import generate_password_hash, check_password_hash

Admins = db.Admins


class Admin:
    def __init__(self, username):
        self.username = username
        usr = Admins.find_one({'username': username})
        self.id = usr['id']
        self.permissions = usr['has_perm']
        self.is_authenticated = True
        self.urole="admin"

    # login manager
    def is_authenticated(self):
        return self.authenticated

    # permission check
    def has_perm(self):
        return self.permissions

    # get the role type of the user
    def get_urole(self):
        return self.urole

    

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        # print("<<<User get_id: ",self.username)
        return self.username

    # set uid
    @staticmethod
    def setUID():
        temp = uid()
        return temp.__str__()

    # password hash
    @staticmethod
    def setHash(pw):
        return generate_password_hash(pw)

    @staticmethod
    def checkPassword(hash, pw):
        return check_password_hash(hash, pw)
