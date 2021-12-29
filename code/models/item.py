from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    # ForeignKey hace link al key de la tabla de stores. Asi se asocian los items a un store. Para borrar ese store,
    # es necesario borrar antes todos los items asociados.
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')  # Esta store es la que corresponde al store_id

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()  # SELECT * FROM items WHERE name=name LIMIT 1 (devuelve la primera fila)

    # session.add modifica el objeto de la sesioón y lo envía a la bbdd, por lo que vale para crear y editar (insert and update)
    def save_to_db(self):
        db.session.add(self)  # La sesión agrupa todos los objetos que quiera, y los puedo añadir todos juntos a la bbdd
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
