import json
from django.test import TestCase
from .models import Seller, SellerHandle

class TestSellerByIdView(TestCase):
    def test_get_a_seller_by_id_with_known_id(self):
        seller = Seller(name="test seller name")
        seller.save()

        handle = SellerHandle(seller=seller, name="test-seller")
        handle.save()

        response = self.client.get('/api/sellers/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {
            'id': 1,
            'name': 'test seller name',
            'handle': 'test-seller'
        })

    def test_get_a_seller_by_id_with_unknown_id(self):
        response = self.client.get('/api/sellers/199/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.content), {
            'error': 'seller not found'
        })

    def test_update_seller_handle_not_implemented(self):
        seller = Seller(name="test seller name")
        seller.save()

        handle = SellerHandle(seller=seller, name="test-seller")
        handle.save()

        response = self.client.put(
            '/api/sellers/1/',
            content_type='application/json',
            data=json.dumps({
                'handle': 'new-handle'
            })
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {
            'id': 1,
            'name': 'test seller name',
            'handle': 'new-handle'
        })


class TestSellerByHandleView(TestCase):
    def test_get_a_seller_by_handle_with_known_handle(self):
        seller = Seller(name="test seller name")
        seller.save()

        handle = SellerHandle(seller=seller, name="test-seller")
        handle.save()

        response = self.client.get('/api/sellers/handle/test-seller/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {
            'id': 1,
            'name': 'test seller name',
            'handle': 'test-seller'
        })

    def test_get_a_seller_by_id_with_unknown_handle(self):
        response = self.client.get('/api/sellers/handle/unknown-handle/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.content), {
            'error': 'seller not found'
        })
