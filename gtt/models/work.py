from gtt import db
from gtt.models import Technique, WorkLink, LinkType

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
            self._create()
            return
        conn = db.get_db()
        cur = conn.cursor()
        cur.execute("""UPDATE "work" SET
                        "name" = ?
                       WHERE "id" = ?""", \
                       (self.name, self.id))

    def _create(self):
        """Insert this work into the DB"""
        conn = db.get_db()
        cur = conn.cursor()
        cur.execute("""INSERT INTO "work" (
                        "name"
                        ) VALUES (?)""", \
                       (self.name,))
        # The comma after name is to force it to be a tuple, as Sqlite3 requires
        self.id = cur.lastrowid

    def remove(self):
        """Remove this work from the DB"""
        # Do not delete links etc - ON DELETE CASCADE in the DB
        conn = db.get_db()
        cur = conn.cursor()
        cur.execute("""DELETE FROM "work" WHERE "id" = ?""", \
                       (self.id,))
        self.id = None

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

    def techniques(self):
        """Get a list of required techniques to play this work from the
           database"""
        if self.id is None:
            # If not saved, no saved techniques yet
            return []

        conn = db.get_db()
        cur = conn.cursor()
        cur.execute(""" SELECT "technique".* FROM "technique"
                        LEFT JOIN "work_technique"
                        ON "work_technique"."technique_id" = "technique"."id"
                        WHERE "work_technique"."work_id" = ? """, \
                        (str(self.id),))
        result = cur.fetchall()
        return [Technique.from_row(i) for i in result]

    def add_technique(self, technique_to_add):
        """Add a technique required to perform the work"""
        if self.id is None:
            raise ReferenceError("Must save work before adding technique")
        conn = db.get_db()
        cur = conn.cursor()
        cur.execute("""INSERT INTO "work_technique" (
                        "work_id",
                        "technique_id"
                        ) VALUES (?, ?)""", \
                    (str(self.id), str(technique_to_add.id)))

    def remove_technique(self, technique_to_remove):
        """Remove a technique required to perform the work"""
        if self.id is None:
            raise ReferenceError("Must save work before removing technique")
        conn = db.get_db()
        cur = conn.cursor()
        cur.execute("""DELETE FROM "work_technique" WHERE
                        "work_id" = ? AND
                        "technique_id" = ?)""", \
                        (str(self.id), str(technique_to_remove.id)))

    def links(self):
        """Get the list of links for this work from the database"""
        return WorkLink.find_by_work(self)

    def add_link(self, href: str, link_type: LinkType):
        """Add a link to this work to the database"""
        if self.id is None:
            raise ReferenceError("Must save work before removing technique")
        link_to_add = WorkLink()
        link_to_add.link_type = link_type
        link_to_add.href = href
        link_to_add.work_id = self.id
        link_to_add.save()

    def remove_link(self, link: WorkLink):
        """Remove a link from the database"""
        link.remove_link(self)
