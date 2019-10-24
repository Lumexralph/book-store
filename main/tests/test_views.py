from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from main.models import Product


class TestPage(TestCase):
    def test_home_page_works(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, 'BookStore')

    def test_about_us_page_works(self):
        response = self.client.get(reverse('about_us'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about_us.html')
        self.assertContains(response, 'BookStore')

    def test_products_page_returns_active(self):
        Product.objects.create(
            name='The cathedral and the bazaar',
            slug='cathedral-bazaar',
            price=Decimal('10.00'),
        )
        Product.objects.create(
            name='A Tale of Two Cities',
            slug='tale-two-cities',
            price=Decimal('2.00'),
            active=False,
        )

        product_list = Product.objects.active().order_by(
            'name'
        )
        response = self.client.get(
            reverse('products', kwargs={'tag': "all"})
        )

        self.assertEqual(
            list(response.context['object_list']),
            list(product_list),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'BookStore')

    def test_products_page_filters_by_tag_and_active(self):
        cb = Product.objects.create(
            name='The cathedral and the bazaar',
            slug='cathedral-bazaar',
            price=Decimal('10.00'),
        )
        cb.tags.create(name='Open Source', slug='open-source')
        Product.objects.create(
            name='A Tale of Two Cities',
            slug='tale-two-cities',
            price=Decimal('2.00'),
            active=False,
        )

        response = self.client.get(
            reverse('products', kwargs={'tag': 'open-source'})
        )
        product_list = (
            Product.objects.active()
            .filter(tags__slug='open-source')
            .order_by('name')
        )

        self.assertEqual(
            list(response.context['object_list']),
            list(product_list),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'BookStore')