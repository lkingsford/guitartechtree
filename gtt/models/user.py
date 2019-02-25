from gtt import db

class User:
    """A user of GTT
    """
    def __init__(self):
        """Create a blank user"""
        self.id = None
        self.username = None
        self.hashed_password = None
        self.can_su = False
        self.can_manage_works = False
        self.can_manage_users = False

    def to_session(self):
        """Save a user object to the session"""
        return { 'username': self.username }

    @classmethod
    def from_session(cls, session_dict):
        """Get a User object from the session"""
        user = User()
        user.id = session_dict.get('id', user.id)
        user.username = session_dict.get('username', user.username)
        user.hashed_password = session_dict.get('hashed_password',
                user.hashed_password)
        return user

    @classmethod
    def from_row(cls, result_row):
        """Instantiate a user from a row dict"""
        user = User()
        user.id = result_row['id']
        user.username = result_row['username']
        user.hashed_password = result_row['hashed_password']
        user.can_su = result_row['can_su'] == 1
        user.can_manage_works = result_row['can_manage_works'] == 1
        user.can_manage_techniques = result_row['can_manage_techniques'] == 1
        return user

    def save(self):
        """Save this user to the DB"""
        if self.id is None:
            self.create()
            return
        conn = db.get_db()
        cur = conn.cursor()
        cur.execute("""UPDATE "user" SET
                        "username" = ?,
                        "hashed_password" = ?,
                        "can_su" = ?,
                        "can_manage_works" = ?,
                        "can_manage_techniques" = ?
                       WHERE "id" = ?""", \
                       (self.username, self.hashed_password, self.can_su,
                        self.can_su, self.can_manage_works,
                        self.can_manage_techniques, self.id))

    def create(self):
        """Insert this user into the DB"""
        conn = db.get_db()
        cur = conn.cursor()
        cur.execute("""INSERT INTO "user" (
                        username,
                        hashed_password,
                        can_su,
                        can_manage_works,
                        can_manage_techniques) VALUES (?, ?, ?, ?, ?)""", \
                        (self.username, self.hashed_password, self.can_su,
                         self.can_manage_works, self.can_manage_techniques))
        self.id = cur.lastrowid

    @classmethod
    def find(cls, username = None, id = None):
        """Find a given user in the DB"""
        if username is None and id is None:
            raise UnboundLocalError('username or id must be defined')
        if username is not None and id is not None:
            raise ValueError('Only one of username or id can be defined')

        conn = db.get_db()
        cur = conn.cursor()

        if username is not None:
            cur.execute("SELECT * FROM user WHERE username=?", username)
        elif id is not None:
            cur.execute("SELECT * FROM user WHERE id=?", str(id))

        result = cur.fetchone()
        if result is not None:
            return User.from_row(result)
        else:
            return None
