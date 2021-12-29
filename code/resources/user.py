import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
from db import db


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="This field can not be blank!"
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="This field can not be blank!"
    )

    def post(self):
        # parse_args recupera los datos de add_argumen (username, password) y los añade a data en forma de diccionario (key-value)
        data = UserRegister.parser.parse_args()  # Esto es parte de flask_Restful: es lo que coge los datos de la web

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists."}, 400

        user = UserModel(**data)  # user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {"message": "User created successfully!"}, 201
