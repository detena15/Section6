import sqlite3


class UserModel:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):  # Search into the database by 'username'
        con = sqlite3.connect('data.db')
        cursor = con.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))  # you have to send a list -> (username,)
        row = result.fetchone()  # Just get the first row out of that result set
        if row:
            # user = cls(row[0], row[1], row[2])  # Create a new User object called user, with the values of the row
            user = cls(*row)
        else:
            user = None  # Create a User object with None

        con.close()
        return user

    @classmethod
    def find_by_id(cls, _id):  # Search into the database by 'username'
        con = sqlite3.connect('data.db')
        cursor = con.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))  # you have to send a list -> (username,)
        row = result.fetchone()  # Just get the first row out of that result set
        if row:
            # user = cls(row[0], row[1], row[2])  # Create a new User object called user, with the values of the row
            user = cls(*row)
        else:
            user = None  # Create a User object with None

        con.close()
        return user
