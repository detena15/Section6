import sqlite3
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse


class Item(Resource):
    # Parser here: that is the way of making that it belongs to the class, and not to any def. Now, it parser all the
    # REST methods
    # This object is going to parse the request
    parser = reqparse.RequestParser()
    # Parser is going to look in the JSON payload, but it also look in, for example, form payloads (HTML forms)
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field can not be blank!"
    )

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)

        if item:
            return item

        return {'message': 'Item not found'}, 4

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {"item": {"name": row[0], "price": row[1]}}

    def post(self, name):
        if self.find_by_name(name):
            return {'message': f"An item with name {name} already exists."}, 400

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}

        try:
            self.insert(item)
        except sqlite3.OperationalError:
            return {'message': "An error occurred inserting the item."}, 500  # Internal Server Error

        return item, 201

    @classmethod
    def insert(cls, item):
        con = sqlite3.connect('data.db')
        cursor = con.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        con.commit()
        con.close()

    def delete(self, name):
        con = sqlite3.connect('data.db')
        cursor = con.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        con.commit()
        con.close()

        return {'message': 'Item deleted'}

    def put(self, name):  # Put updates an existing item. If it does not exist, it is created
        data = Item.parser.parse_args()

        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        if item is None:
            try:
                self.insert(updated_item)
            except sqlite3.OperationalError:
                return {'message': "An error occurred inserting the item."}, 500
        else:
            try:
                self.update(updated_item)
            except sqlite3.OperationalError:
                return {'message': "An error occurred updating the item."}, 500

        return updated_item

    @classmethod
    def update(cls, item):
        con = sqlite3.connect('data.db')
        cursor = con.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        con.commit()
        con.close()


class ItemList(Resource):
    def get(self):
        con = sqlite3.connect('data.db')
        cursor = con.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        con.close()

        return {'items': items}
