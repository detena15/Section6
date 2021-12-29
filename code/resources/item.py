from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.item import ItemModel


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

    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help="Every item needs a store id."
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()

        return {'message': 'Item not found'}, 4

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f"An item with name {name} already exists."}, 400

        data = Item.parser.parse_args()

        # item = ItemModel(name, data['price'], data['store_id'])
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': "An error occurred inserting the item."}, 500  # Internal Server Error

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted.'}

    def put(self, name):  # Put updates an existing item. If it does not exist, it is created
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            # item = ItemModel(name, data['price'], data['store_id'])
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}  # all() devuelve todos los objetos de la base de datos
