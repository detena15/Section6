from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from code.resources import Item, ItemList
from security import authenticate, identity
from code.resources import UserRegister

# Crear el objeto de la interfaz web
app = Flask(__name__)

# Crear la variable de la key
app.secret_key = 'edu'

# Crear el objeto API
api = Api(app=app)

# Create the object that allow us to check credentials
jwt = JWT(app=app, authentication_handler=authenticate, identity_handler=identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':  # Asi solo se ejecuta si se ejecuta app.py; si se importa no se ejecuta, pues __name__ sera otro
    app.run(port=5000, debug=True)
