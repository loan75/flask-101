# tests/test_views.py
from flask_testing import TestCase
from wsgi import PRODUCTS
from wsgi import app


class TestViews(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_products_json(self):
        response = self.client.get("/api/v1/products")
        products = response.json
        self.assertIsInstance(products, dict)
        self.assertGreater(len(products), 2)

    def test_read_ok(self):
        response = self.client.get("/api/v1/products/1")
        product = response.json
        self.assertIsInstance(product, dict)
        self.assertGreater(len(product), 1)
        self.assert_200(response)
        self.assertDictEqual(product, PRODUCTS[1])

    def test_read_ko(self):
        response = self.client.get("/api/v1/products/999")
        product = response.json
        self.assertIsInstance(product, dict)
        self.assert_404(response)
