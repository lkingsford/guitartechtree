from gtt import db

class Work:
    """A work that can be learned by a user
    """
    def __init__(self):
        """Create a blank work"""
        self.id = None
        self.name = None

    @classmethod
    def from_row(cls, result_row):
        """Instantiate a work from a row dict"""
        work = Work()
        work.id = result_row['id']
        work.name = result_row['name']
        return work

    def save(self):
        """Save this work to the DB"""
        if self.id is None:
            self.create()
            return
        conn = db.get_db()
        cur = conn.cursor()
        cur.execute("""UPDATE "work" SET
                        "name" = ?
                       WHERE "id" = ?""", \
                       (self.name, self.id))

    def create(self):
        """Insert this work into the DB"""
        conn = db.get_db()
        cur = conn.cursor()
        cur.execute("""INSERT INTO "work" (
                        "name"
                        ) VALUES (?)""", \
        # The comma after name is to force it to be a tuple, as Sqlite3 requires
                       (self.name,))
        self.id = cur.lastrowid

    @classmethod
    def find(cls, work_id):
        """Find a given work in the DB"""
        if work_id is None:
            raise UnboundLocalError('work_id must be defined')

        conn = db.get_db()
        cur = conn.cursor()

        cur.execute("SELECT * FROM work WHERE id=?", str(work_id))

        result = cur.fetchone()
        if result is not None:
            return Work.from_row(result)
        else:
            return None
