import sqlite3
from flask_restful import Resource, reqparse

from code.models.user import UserModel


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
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists."}, 400

        con = sqlite3.connect('data.db')
        cursor = con.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"  # El NULL hace referencia al id, que no es necesario enviarlo pues es incremental y automatico
        cursor.execute(query, (data['username'], data['password']))

        con.commit()
        con.close()

        return {"message": "User created successfully!"}, 201
