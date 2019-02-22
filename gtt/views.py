from gtt import app
from gtt import db

@app.route("/test")
def test1():
    conn = db.get_db()
    conn.execute('CREATE TABLE "user" ("user_id" INTEGER PRIMARY KEY ASC)')
    conn.commit()
    return "Trial and fury"
