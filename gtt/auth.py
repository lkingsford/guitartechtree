from flask import session
from gtt import db
from gtt.models import User

def _unauthorized_default():
    return "Unauthorized"

unauthorized = _unauthorized_default

def login(username, password):
    if username != 'fail':
        user = User()
        session['user'] = user.to_session()
        return user
    else:
        return None

def logged_in(func):
    def func_wrapper(*args, **kwargs):
        if 'user' not in session:
            return unauthorized()
        else:
            return func(*args, **kwargs)
    return func_wrapper
