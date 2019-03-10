from flask import Flask

app = Flask(__name__, instance_relative_config=True,
    static_url_path='/static')
app.config.from_object('config')
app.config.from_pyfile('config.py')
app.secret_key = app.config['SESSION_SECRET_KEY']

from gtt import views
