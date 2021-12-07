import sqlite3


class ItemModel:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return cls(*row)
            # return cls(row[0], row[1])  # __init__ method

    def insert(self):
        con = sqlite3.connect('data.db')
        cursor = con.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (self.name, self.price))

        con.commit()
        con.close()

    def update(self):
        con = sqlite3.connect('data.db')
        cursor = con.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (self.name, self.price))

        con.commit()
        con.close()
