from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from resources.item import Item, ItemList
from resources.user import UserRegister
from resources.store import Store, StoreList
from security import authenticate, identity
from db import db

# Crear el objeto de la interfaz web
app = Flask(__name__)
# Le dices a sqlalchemy donde va a dejar los datos de la base de datos, en nuestro proyecto
# puede ser sqlite, mysql, psgresql, oracle, ...
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

# Por defecto SQLALQUEMY hace un seguimiento de los cambios en los objetos. Esto solo deja la función básica.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Crear la variable de la key
app.secret_key = 'edu'

# Crear el objeto API
api = Api(app=app)


# Este decorador viene con flask. Se va a ejecutar antes de la primera request
@app.before_first_request
def create_tables():
    db.create_all()
    # Crea data.db si no existe. Pero solo crea las tablas que vea: por ejemplo, al importar Store resource,
    # a su vez importa StoreModel, siendo esta la clase que crea la tabla


# Create the object that allow us to check credentials
jwt = JWT(app=app, authentication_handler=authenticate, identity_handler=identity)

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':  # Asi solo se ejecuta si se ejecuta app.py; si se importa no se ejecuta, pues __name__ sera otro
    db.init_app(app)
    app.run(port=5000, debug=True)
