from typing import Dict
from flask import Response, redirect, request, render_template, url_for
from gtt import app
from gtt import db
from gtt import auth
from gtt.models import User, LoginFailedError, Technique, Work

def state()->Dict[str, str]:
    """Get parameters to pass to all pages"""
    return {'user':auth.session_user()}

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
    return render_template('login_page.j2', **state())

@app.route("/")
def index():
    return render_template('index.j2', **state())

@app.route("/about")
def about():
    return render_template('about.j2', **state())

@app.route("/technique/<technique_id>")
def view_technique(technique_id):
    """View a given technique"""
    return render_template('technique.j2',
        technique=Technique.find(technique_id),
        **state())

@app.route("/technique/<technique_id>/edit")
def edit_technique(technique_id):
    """Edit a given technique"""
    if auth.session_user().can_manage_techniques:
        return render_template('edit_technique.j2',
                technique=Technique.find(technique_id),
                **state())
    return Response('User not logged in or not authorized to manage techniques.',
        401)

@app.route("/technique/new")
@auth.logged_in
def new_technique():
    """Create a technique"""
    if auth.session_user().can_manage_techniques:
        return render_template('edit_technique.j2',
                technique=None,
                **state())
    return Response('User not logged in or not authorized to manage techniques.',
        401)

@app.route("/technique/<technique_id>", methods=["POST"])
@auth.logged_in
def save_technique(technique_id):
    """Save a given technique"""
    if not auth.session_user().can_manage_techniques:
        return Response('User not logged in or not authorized to manage techniques.',
                401)
    if int(technique_id) == -1:
        # New work
        technique = Technique()
    else:
        # Existing technique
        technique = Technique.find(technique_id)
    technique.name = request.form['name']
    technique.short_description = request.form['short_description']
    technique.save()
    db.get_db().commit()
    return redirect(url_for("view_technique", technique_id=technique.id))

@app.route("/work/<work_id>/edit")
def edit_work(work_id):
    """Edit a work"""
    if auth.session_user().can_manage_works:
        return render_template('edit_work.j2',
                work=Work.find(work_id),
                **state())
    return Response('User not logged in or not authorized to manage works.',
        401)

@app.route("/work/<work_id>")
def view_work(work_id):
    """View a work"""
    return render_template('work.j2',
        work=Work.find(work_id),
        **state())

@app.route("/work/<work_id>", methods=['POST'])
@auth.logged_in
def save_work(work_id):
    """Save a work"""
    if not auth.session_user().can_manage_works:
        return Response('User not logged in or not authorized to manage works.',
                401)
    if int(work_id) == -1:
        # New work
        work = Work()
    else:
        # Existing work
        work = Work.find(work_id)
    work.name = request.form['name']
    work.save()
    db.get_db().commit()
    return redirect(url_for("view_work", work_id=work.id))

@app.route("/work/new")
@auth.logged_in
def new_work():
    """Create a work"""
    if auth.session_user().can_manage_works:
        return render_template('edit_work.j2',
                work=None,
                **state())
    return Response('User not logged in or not authorized to manage works.',
        401)

@app.route("/work_list")
def work_list():
    """List works"""
    return render_template('work_list.j2',
                           works=Work.find_all(),
                           **state())

@app.route("/technique_list")
def technique_list():
    """List techniques"""
    return render_template('technique_list.j2',
                            techniques=Technique.find_all(),
                            **state())