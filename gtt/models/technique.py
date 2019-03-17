from gtt import db

class Technique:
    """A technique that a player can use to play something
    """
    def __init__(self):
        """Create a blank technique"""
        self.id = None
        self.name = None
        self.short_description = None

    @classmethod
    def from_row(cls, result_row):
        """Instantiate a technique from a row dict"""
        technique = Technique()
        technique.id = result_row['id']
        technique.name = result_row['name']
        technique.short_description = result_row['short_description']
        return technique

    def save(self):
        """Save this technique to the DB"""
        if self.id is None:
            self._create()
            return
        conn = db.get_db()
        cur = conn.cursor()
        cur.execute("""UPDATE "technique" SET
                        "name" = ?,
                        "short_description" = ?
                       WHERE "id" = ?""", \
                       (self.name, self.short_description, self.id))

    def _create(self):
        """Insert this technique into the DB"""
        conn = db.get_db()
        cur = conn.cursor()
        cur.execute("""INSERT INTO "technique" (
                        "name",
                        "short_description") VALUES (?, ?)""", \
                       (self.name, self.short_description))
        self.id = cur.lastrowid

    @classmethod
    def find(cls, technique_id):
        """Find a given technique in the DB"""
        if technique_id is None:
            raise UnboundLocalError('technique_id must be defined')

        conn = db.get_db()
        cur = conn.cursor()

        cur.execute("SELECT * FROM technique WHERE id=?", str(technique_id))

        result = cur.fetchone()
        if result is not None:
            return Technique.from_row(result)
        return None

    @classmethod
    def find_all(cls):
        """Find all works in the DB"""
        conn = db.get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM technique ORDER BY name")
        return [Technique.from_row(row) for row in cur]