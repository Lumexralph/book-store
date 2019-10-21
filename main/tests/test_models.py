from decimal import Decimal
from django.test import TestCase

from main.models import Product


class TestModel(TestCase):
    def test_active_manager_works(self):
        Product.objects.bulk_create([
            Product(
                name='The cathedral and the bazaar',
                price=Decimal('10.0'),
            ),
            Product(
                name='Pride and Prejudice',
                price=Decimal('4.0'),
            ),
            Product(
                name='A Tale of Two Cities',
                price=Decimal('16.0'),
                active=False,
            ),
        ])

        self.assertEqual(len(Product.objects.active()), 2)
