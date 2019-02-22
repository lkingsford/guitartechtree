from gtt import db

class User:
    def __init__(self, source = None):
        self.user_id = None
        self.username = None
        self.hashed_password = None

    def to_session(self):
        return { 'username': self.username }

    @classmethod
    def from_session(cls, source):
            self.user_id = source.get('user_id', self.user_id)
            self.username = source.get('username', self.username)
            self.hashed_password = source.get('hashed_password',
                    self.hashed_password)

    @classmethod
    def from_row(cls, result_row):
        user = User()
        user.id = result_row[0]
        user.username = result_row[1]
        user.hashed_password = result_row[2]
        return user

    @classmethod
    def find(cls, username = None, user_id = None):
        if username is None and user_id is None:
            raise ArgumentError('username or user_id must be defined')
        if username is not None and user_id is not None:
            raise ArgumentError('Only one of username or user_id can be defined')

        conn = db.get_db()
        cur = conn.cursor()

        if username is not None:
            cur.execute("SELECT * FROM user WHERE username=?", username)
        elif user_id is not None:
            cur.execute("SELECT * FROM user WHERE user_id=?", user_id)

        result = cur.fetchone()
        if result is not None:
            print("DB result is ", result)
            return User.from_row(result)
        else:
            return None
