from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    # self.items se ha convertido en un query builder al que aplicar all(). Esto es asi por haber añadido a items -> lazy='dynamics'

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
