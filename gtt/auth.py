from flask import session
from gtt.models import User

def _unauthorized_default():
    return "Unauthorized"

unauthorized = _unauthorized_default

def login(username, password):
    user = User.attempt_login(username, password)
    session['user'] = user.to_session()
    return user

def logged_in(func):
    def func_wrapper(*args, **kwargs):
        if 'user' not in session:
            return unauthorized()
        else:
            return func(*args, **kwargs)
    return func_wrapper
