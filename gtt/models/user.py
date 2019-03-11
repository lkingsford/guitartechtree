from passlib.hash import argon2
from gtt import db

class LoginFailedError(Exception):
    """Error used if username or password isn't a match"""
    pass

class User:
    """A user of GTT
    """
    def __init__(self):
        """Create a blank user
        These are also used for the default user if no user is logged in"""
        self.id = None
        self.username = None
        self.hashed_password = None
        self.can_su = False
        self.can_manage_works = False
        self.can_manage_users = False
        self.can_manage_techniques = False

    def to_session(self):
        """Save a user object to the session"""
        return { 'username': self.username,
                 'id': self.id,
                 'can_su': self.can_su,
                 'can_manage_works': self.can_manage_works,
                 'can_manage_users': self.can_manage_users,
                 'can_manage_techniques': self.can_manage_techniques }

    def set_password(self, password):
        """Set the hash password from a given password"""
        self.hashed_password = argon2.hash(password)

    @classmethod
    def from_session(cls, session_dict):
        """Get a User object from the session"""
        user = User()
        user.id = session_dict.get('id', user.id)
        user.username = session_dict.get('username', user.username)
        user.can_su = session_dict.get('can_su', user.can_su)
        user.can_manage_works = session_dict.get('can_manage_works',
            user.can_manage_works)
        user.can_manage_techniques = session_dict.get('can_manage_works',
            user.can_manage_techniques)
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
            self._create()
            return
        conn = db.get_db()
        cur = conn.cursor()
        cur.execute("""UPDATE "user" SET
                        "username" = ?,
                        "hashed_password" = ?,
                        "can_su" = ?,
                        "can_manage_works" = ?,
                        "can_manage_techniques" = ?
                       WHERE "id" = ?""",
                       (self.username, self.hashed_password, self.can_su,
                        self.can_manage_works, self.can_manage_techniques,
                        self.id))

    def _create(self):
        """Insert this user into the DB"""
        conn = db.get_db()
        cur = conn.cursor()
        cur.execute("""INSERT INTO "user" (
                        username,
                        hashed_password,
                        can_su,
                        can_manage_works,
                        can_manage_techniques) VALUES (?, ?, ?, ?, ?)""",
                        (self.username, self.hashed_password, self.can_su,
                         self.can_manage_works, self.can_manage_techniques))
        self.id = cur.lastrowid

    def remove(self):
        """Remove this user from the DB"""
        conn = db.get_db()
        cur = conn.cursor()
        cur.execute("""DELETE FROM "user" WHERE "id" = ?""",
            (self.id,))
        self.id = None

    @classmethod
    def find(cls, username=None, user_id=None):
        """Find a given user in the DB"""
        if username is None and user_id is None:
            raise UnboundLocalError('username or id must be defined')
        if username is not None and user_id is not None:
            raise ValueError('Only one of username or id can be defined')

        conn = db.get_db()
        cur = conn.cursor()

        if username is not None:
            cur.execute('SELECT * FROM user WHERE username=? COLLATE NOCASE', (username,))
        elif id is not None:
            cur.execute('SELECT * FROM user WHERE id=?', (user_id,))

        result = cur.fetchone()
        if result is not None:
            return User.from_row(result)
        else:
            return None

    @classmethod
    def attempt_login(cls, username, hashed_password):
        """Attempt to login, and raise an error if fail"""
        user = User.find(username=username)
        if user is None:
            raise LoginFailedError('Username not found')
        if argon2.verify(hashed_password, user.hashed_password):
            return user
        raise LoginFailedError('Password incorred')
