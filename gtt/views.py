from flask import Response, redirect, request, render_template, url_for
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
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    auth.logout()
    return redirect(url_for("index"))

@app.route("/login_page")
def login_page():
    return render_template('login_page.j2', user=auth.session_user())

@app.route("/")
def index():
    return render_template('index.j2', user=auth.session_user())

@app.route("/about")
def about():
    return render_template('about.j2', user=auth.session_user())