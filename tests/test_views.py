# tests/test_views.py
from flask_testing import TestCase
from flask import json
from wsgi import PRODUCTS, app


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

    def test_create_ok(self):
        response = self.client.post("/api/v1/products", data=json.dumps({"name": "lolo"}),
                                    headers={'Content-Type': 'application/json'})
        self.assertIsInstance(PRODUCTS, dict)
        self.assertGreater(len(PRODUCTS), 3)
        self.assertEqual(response.status_code, 201)

    def test_create_ko(self):
        response = self.client.post("/api/v1/products", data=json.dumps({"toto": "toto"}),
                                    headers={'Content-Type': 'application/json'})
        self.assertIsInstance(PRODUCTS, dict)
        self.assertGreater(len(PRODUCTS), 2)
        self.assertEqual(response.status_code, 400)

    def test_update_ok(self):
        response = self.client.put("/api/v1/products/1", data=json.dumps({"name": "toto"}),
                                   headers={'Content-Type': 'application/json'})
        self.assertIsInstance(PRODUCTS, dict)
        self.assertGreater(len(PRODUCTS), 2)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(PRODUCTS[1]["name"], "toto")

    def test_update_ko(self):
        response = self.client.put("/api/v1/products/999", data=json.dumps({"name": "toto"}),
                                   headers={'Content-Type': 'application/json'})
        self.assertIsInstance(PRODUCTS, dict)
        self.assertGreater(len(PRODUCTS), 2)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(PRODUCTS[1]["name"], "Skello")

    def test_update_empty_name_ko(self):
        response = self.client.put("/api/v1/products/999", data=json.dumps({"name": ""}),
                                   headers={'Content-Type': 'application/json'})
        self.assertIsInstance(PRODUCTS, dict)
        self.assertGreater(len(PRODUCTS), 2)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(PRODUCTS[1]["name"], "Skello")
