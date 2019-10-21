from django.test import TestCase
from django.core.files.images import ImageFile
from decimal import Decimal

from main.models import Product, ProductImage


class TestSignal(TestCase):
    def test_thumbnail_are_generated_on_save(self):
        product = Product(
            name='The Cathedral and the bazaar',
            price=Decimal('10.00'),
        )
        product.save()

        with open(
            'main/fixtures/the-cathedral-the-bazaar.jpg',
                'rb') as f:
            image = ProductImage(
                product=product,
                image=ImageFile(f, name='tctb.jpg'),
            )
            with self.assertLogs('main', level='INFO') as cm:
                image.save()
                self.assertGreaterEqual(len(cm.output), 1)
                image.refresh_from_db()

                with open(
                    'main/fixtures/the-cathedral-the-bazaar.thumb.jpg',
                    'rb',
                ) as f:
                    expected_content = f.read()
                    self.assertEqual(expected_content, image.thumbnail.read())
                    image.thumbnail.delete(save=False)
                    image.image.delete(save=False)