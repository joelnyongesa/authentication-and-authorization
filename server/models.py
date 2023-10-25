from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
bcrypt = Bcrypt()

class Owner(db.Model, SerializerMixin):

    __tablename__ = 'owners'

    serialize_rules = ('-cars.owner', )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String)

    # relationships
    cars = db.relationship('Car', backref='owner')

    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password hash cannot be viewed")

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8')
        )
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8')
        )


class Car(db.Model, SerializerMixin):

    __tablename__ = 'cars'

    serialize_rules = ('-owner.cars', )

    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String)

    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'))