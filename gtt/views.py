from flask import Response, request, render_template
from gtt import app
from gtt import db
from gtt import auth
from gtt.models import User, LoginFailedError, Technique, Work

@app.route("/login", methods=['POST'])
def login():
    """Login with given POST method"""
    try:
        user = auth.login(request.form['username'], request.form['password'])
    except LoginFailedError:
        return Response('Login failed. Username or password incorrect.', 401)
    return Response('Login successful')

@app.route("/technique/<technique_id>")
def view_technique(technique_id):
    """View a given technique"""
    return render_template('technique.j2',
        technique=Technique.find(technique_id),
        user=auth.session_user())

@app.route("/technique/new")
@auth.logged_in
def new_technique(technique_id):
    """Create a technique"""
    if auth.session_user().can_manage_techniques:
        return render_template('technique.j2',
                technique=None,
                user=auth.session_user())
    return Response('User not logged in or not authorized to manage techniques.',
        401)

@app.route("/work/<work_id>")
def view_work(work_id):
    """View a work"""
    return render_template('work.j2',
        work=Work.find(work_id),
        user=auth.session_user())

@app.route("/work/new")
@auth.logged_in
def new_work():
    """Create a work"""
    if auth.session_user().can_manage_works:
        return render_template('work.j2',
                work=None,
                user=auth.session_user())
    return Response('User not logged in or not authorized to manage works.',
        401)

@app.route("/")
def index():
    """Return index page"""
    return render_template('index.j2')

@app.route("/about")
def about():
    """Return the about page"""
    return render_template('about.j2')