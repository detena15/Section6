from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    """
    endpoints: get, post, delete
    """
    def get(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            return store.json()

        return {'message': 'Store not found.'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': f'A store with name {name} is already exists.'}, 400

        store = StoreModel(name=name)

        try:
            store.save_to_db()
        except:
            return {'message': 'An error occurred while creating the store'}, 500  # Internal server error

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name=name)

        if store:
            store.delete_from_db()
            return {'message': f'The store {name} was deleted.'}

        return {'message': f'There was no store with the name {name}.'}


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
