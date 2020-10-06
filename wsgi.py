# wsgi.py
# pylint: disable=missing-docstring
from flask import Flask, jsonify, request
import itertools

app = Flask(__name__)
PRODUCTS = {
    1: {'id': 1, 'name': 'Skello' },
    2: {'id': 2, 'name': 'Socialive.tv'},
    3: {'id': 3, 'name': 'Le Wagon'},
}
START_INDEX = len(PRODUCTS) + 1
IDENTIFIER_GENERATOR = itertools.count(START_INDEX)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/api/v1/products', methods=['GET', 'POST'])
def products():
    if request.method == 'GET':
        return jsonify(PRODUCTS)
    if request.method == 'POST':
        product_to_add = request.get_json().get('name', None)
        if product_to_add is None or product_to_add == '':
            return jsonify(), 400
        next_id = next(IDENTIFIER_GENERATOR)
        PRODUCTS[next_id] = {'id': next_id, 'name': product_to_add}
        return jsonify(PRODUCTS), 201


@app.route('/api/v1/products/<int:product_id>', methods=['GET', 'DELETE', 'PUT'])
def product(product_id):
    if request.method == 'GET':
        my_product = PRODUCTS.get(product_id, None)
        if my_product is None:
            return jsonify(), 404
        else:
            return jsonify(my_product)
    if request.method == 'DELETE':
        my_product = PRODUCTS.get(product_id, None)
        if my_product is None:
            return jsonify(), 404
        else:
            PRODUCTS.pop(product_id)
            return jsonify(), 204
    if request.method == 'PUT':
        my_product = PRODUCTS.get(product_id, None)
        new_name = request.get_json().get('name', None)
        if my_product is None or new_name is None or new_name == '':
            return jsonify(), 422
        else:
            PRODUCTS[product_id]['name'] = new_name
            return jsonify(), 204
