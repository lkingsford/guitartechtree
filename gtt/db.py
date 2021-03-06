import sqlite3

from gtt import app
from flask import g

def create_sqlite3(path):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


db_name_to_create = {
        "sqlite3": create_sqlite3
        }


def get_db():
    if 'db' not in g:
        db_path = app.config["DB_PATH"]
        db_driver = app.config["DB_DRIVER"]
        g.db = db_name_to_create[db_driver](db_path)
    return g.db


@app.teardown_appcontext
def teardown_db(error_code):
    db = g.pop('db', None)
    if db is not None:
        db.close()
