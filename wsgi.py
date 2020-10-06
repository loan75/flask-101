# wsgi.py
# pylint: disable=missing-docstring

from flask import Flask, jsonify, abort
app = Flask(__name__)
PRODUCTS = {
    1: {'id': 1, 'name': 'Skello' },
    2: {'id': 2, 'name': 'Socialive.tv'},
    3: {'id': 3, 'name': 'Le Wagon'},
}


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/api/v1/products')
def products():
    return jsonify(PRODUCTS)


@app.route('/api/v1/products/<int:product_id>')
def product(product_id):
    my_product = PRODUCTS.get(product_id, None)
    if my_product is None:
        return jsonify(), 404
    else:
        return jsonify(my_product)
