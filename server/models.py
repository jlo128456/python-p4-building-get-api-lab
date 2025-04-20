from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

# Naming convention for Alembic compatibility
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Bakery(db.Model, SerializerMixin):
    __tablename__ = 'bakeries'

    serialize_rules = ('-baked_goods.bakery',)  # Avoid circular reference

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # One-to-Many relationship
    baked_goods = db.relationship('BakedGood', backref='bakery', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Bakery {self.name}>'

class BakedGood(db.Model, SerializerMixin):
    __tablename__ = 'baked_goods'

    serialize_rules = ('-bakery.baked_goods',)  # Avoid circular reference

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Foreign key linking to Bakery
    bakery_id = db.Column(db.Integer, db.ForeignKey('bakeries.id'))

    def __repr__(self):
        return f'<BakedGood {self.name}, ${self.price}>'
