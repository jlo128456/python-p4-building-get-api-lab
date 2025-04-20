#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def get_bakeries():
    bakeries = db.session.query(Bakery).all()
    return jsonify([bakery.to_dict() for bakery in bakeries]), 200

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = db.session.get(Bakery, id)
    if not bakery:
        abort(404, description=f"Bakery with id {id} not found")
    return jsonify(bakery.to_dict())

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    
    if not goods:
        return jsonify([]), 200  

    return jsonify([good.to_dict() for good in goods]), 200

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if not good:
        abort(404, description="No baked goods found")
    return jsonify(good.to_dict())

if __name__ == '__main__':
    app.run(port=5555, debug=True)
