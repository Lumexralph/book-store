from io import StringIO
import tempfile

from django.core.management import call_command
from django.test import TestCase, override_settings
from main.models import Product, ProductImage, ProductTag


class TestImport(TestCase):
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_import_data(self):
        out = StringIO()
        args = ['main/fixtures/product-sample.csv',
                'main/fixtures/product-sampleimages/']

        call_command('import_data', *args, stdout=out)

        expected_out = ('Importing products...\n'
                        'Products processed=3 (created=3)\n'
                        'Tags processed=6 (created=6)\n'
                        'Images processed=3\n')

        self.assertEqual(out.getvalue(), expected_out)
        self.assertEqual(Product.objects.count(), 3)
        self.assertEqual(ProductTag.objects.count(), 6)
        self.assertEqual(ProductImage.objects.count(), 3)
