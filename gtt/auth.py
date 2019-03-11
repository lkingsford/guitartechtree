from functools import wraps
from flask import session
from gtt.models import User

def _unauthorized_default():
    return "Unauthorized"

unauthorized = _unauthorized_default

def login(username, password):
    """Attempt to login with given credentials, returning the user or raising
    if unsuccessful"""
    user = User.attempt_login(username, password)
    session['user'] = user.to_session()
    return user

def logged_in(f):
    @wraps(f)
    def func_wrapper(*args, **kwargs):
        if 'user' not in session:
            return unauthorized()
        else:
            return f(*args, **kwargs)
    return func_wrapper

def session_user():
    """Return the user that is currently logged in per the session"""
    if 'user' not in session:
        return None
    return User.from_session(session['user'])
