from enum import IntEnum
from gtt import db

class WorkLink:
    """A link attached to a work
    """

    def __init__(self):
        """Create a blank work_link"""
        self.id = None
        self.link_type = None
        # A None link_type can not be saved
        self.href = None
        self.work_id = None

    @classmethod
    def from_row(cls, result_row):
        """Instantiate a work_link from a row dict"""
        work_link = WorkLink()
        work_link.id = result_row['id']
        work_link.link_type = result_row['link_type']
        work_link.href = result_row['href']
        work_link.work_id = result_row['work_id']
        return work_link

    def save(self):
        """Save this work_link to the DB"""
        if self.link_type is None:
            raise ValueError('LinkType must be set')
        if self.id is None:
            self._create()
            return
        conn = db.get_db()
        cur = conn.cursor()
        cur.execute("""UPDATE "work_link" SET
                        "id" = ?,
                        "link_type" = ?,
                        "href" = ?,
                        "work_id" = ?,
                       WHERE "id" = ?""", \
                       (self.id, self.link_type, self.href, self.work_id))

    def _create(self):
        """Insert this work_link into the DB"""
        conn = db.get_db()
        cur = conn.cursor()
        cur.execute("""INSERT INTO "work_link" (
                        "link_type",
                        "href",
                        "work_id") VALUES (?, ?, ?)""", \
                       (self.link_type, self.href, self.work_id))
        self.id = cur.lastrowid

    def remove(self):
        """Remove this work_link from the DB"""
        conn = db.get_db()
        cur = conn.cursor()
        cur.execute("""DELETE FROM "work_link" WHERE "id" = ?""", \
            (self.id,))

    @classmethod
    def find(cls, work_link_id):
        """Find a given work_link in the DB"""
        if work_link_id is None:
            raise UnboundLocalError('work_link_id must be defined')

        conn = db.get_db()
        cur = conn.cursor()

        cur.execute("SELECT * FROM work_link WHERE id=?", str(work_link_id))

        result = cur.fetchone()
        if result is not None:
            return WorkLink.from_row(result)
        else:
            return None

    @classmethod
    def find_by_work(cls, work: "Work"):
        """Find links for a given work"""
        if work is None or work.id is None:
            raise UnboundLocalError('work must be provided and in db')

        conn = db.get_db()
        cur = conn.cursor()

        cur.execute(""" SELECT * FROM "work_link"
                        WHERE "work_id" = ? """, \
                        (str(work.id),))

        result = cur.fetchall()
        return [WorkLink.from_row(i) for i in result]


class LinkType(IntEnum):
    """Types that a link might be"""
    AFFILIATE = 1
    STREAM = 2
