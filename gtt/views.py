from gtt import app
from gtt import db
from gtt import auth
from gtt.models import User

#@app.route("/login", methods=['POST'])
@app.route("/login")
def login():
    #user = auth.login(request.form['username'], request.form['password'])
    user = auth.login('username', 'password')
    if user is not None:
        print('Success')
        return 'Success'
    else:
        print('Login failed')
        return 'Login Failed'

@app.route("/private/<user_id>")
@auth.logged_in
def private(user_id):
    return User.find(user_id=user_id).username
