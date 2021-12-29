"""
Esta clase es una API (no es una API Rest, pero sí una API: Application Programming Interface).
Esta API expone dos endpoints (two methods):
1. find_by_username
2. find_by_id
Ambos métodos forman una interfaz para que otras partes del programa interactúen
con la 'cosa' user. Eso incluye guardar y extraer de la base de datos.
Mientras esta API no se cambie, no hay que preocuparse del impacto de nuestros cambios
en el resto del código.
Por ejemplo, se usan estos endpoint en otro trozo de código del programa: security.py
security.py usa esta interfaz para comunicarse con el usuario y la base de datos
--> primary_key: siempre que se inserte una nueva fila en la base de datos, el motor de SQL usado (SQLite en este caso),
se asignará un id automáticamente (es la razón por la que no se añade al constructor: al crearse la instancia de UserModel,
SQLite hace self.id = <valor incremental>)
"""
from db import db  # Esto también funciona: from .. import db


class UserModel(db.Model):
    # Decir a la bbdd que nombre de tabla va a tener asociada esta clase (y todos los objetos que se instancien de ella)
    __tablename__ = 'users'

    # Decir a la bbdd que tres columnas va a tener
    id = db.Column(db.Integer, primary_key=True)  # Al ser llave primaria, es incremental
    username = db.Column(db.String(80))  # 80 se refiere al máximo número de caracteres
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):  # Search into the database by 'username'
        return cls.query.filter_by(username=username).first()  # SELECT * FROM users WHERE username=username LIMIT 1 (devuelve la primera fila)

    @classmethod
    def find_by_id(cls, _id):  # Search into the database by 'username'
        return cls.query.filter_by(id=_id).first()
