from flask import Response, request, render_template
from gtt import app
from gtt import db
from gtt import auth
from gtt.models import User, LoginFailedError

@app.route("/login", methods=['POST'])
def login():
    """Login with given POST method"""
    try:
        user = auth.login(request.form['username'], request.form['password'])
    except LoginFailedError:
        return Response('Login failed. Username or password incorrect.', 401)
    return Response('Login successful')

@app.route("/private_test/<user_id>")
@auth.logged_in
def private_test(user_id):
    return User.find(user_id=user_id).username

@app.route("/")
def root():
    return render_template('layout.j2', content='Content goes here')

@app.route("/about")
def about():
    return render_template('about.j2')