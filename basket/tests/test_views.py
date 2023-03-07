from importlib import import_module

from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse

from basket.views import basket_summary
from store.models import Category, Product


class TestBasketView(TestCase):
    
    def setUp(self) -> None:
        self.user = User.objects.create(username='admin')
        self.category = Category.objects.create(name='django', slug='django')
        self.prod_1 = Product.objects.create(category=self.category, title='Django initial', created_by=self.user,
                                             author='admin',
                                             description='123', slug='django-initial', price=20.00, image='django.png'
                                             )
        
        self.prod_2 = Product.objects.create(category=self.category, title='Django inter', created_by=self.user,
                                             author='admin',
                                             description='Django 2', slug='django-inter', price=40.00,
                                             image='django.png')
        
        self.prod_3 = Product.objects.create(category=self.category, title='Django advanced', created_by=self.user,
                                             author='admin',
                                             description='Django advanced', slug='django-advanced', price=60.00,
                                             image='django.png')
        
        # adding to basket
        
        self.client.post(
            reverse('basket:basket_add'),
            data={'productId': self.prod_1.id, 'productQty': 1, 'action': 'post'},
            xhr=True)
        
        self.client.post(
            reverse('basket:basket_add'),
            data={'productId': self.prod_2.id, 'productQty': 2, 'action': 'post'},
            xhr=True)
    
    def test_basket_url(self):
        """
        Test basket response status
        """
        response = self.client.get(reverse('basket:basket_summary'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/basket/summary.html')
    
    def test_basket_page(self):
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        resource = basket_summary(request)
        html = resource.content.decode('utf-8')
        
        self.assertIn('<title>Store Basket</title>', html)
        self.assertInHTML('<div id="basket-qty" class="d-inline-block">0</div>', html)
        self.assertInHTML('<div class="h6 fw-bold">Sub Total: $<span id="basket-total">0</span></div>', html)
    
    def test_basket_add(self):
        """Test adding products to basket"""
        
        product = Product.objects.get(slug='django-initial')
        
        response = self.client.post(
            reverse('basket:basket_add'),
            data={'productId': product.id, 'productQty': 1, 'action': 'post'},
            xhr=True)
        self.assertEqual(response.json(), {'qty': '4'})
        
        product = Product.objects.get(slug='django-inter')
        response = self.client.post(
            reverse('basket:basket_add'),
            data={'productId': product.id, 'productQty': 2, 'action': 'post'},
            xhr=True)
        self.assertEqual(response.json(), {'qty': '6'})
        
        product = Product.objects.get(slug='django-advanced')
        response = self.client.post(
            reverse('basket:basket_add'),
            data={'productId': product.id, 'productQty': 1, 'action': 'post'},
            xhr=True)
        self.assertEqual(response.json(), {'qty': '7'})
    
    def test_basket_delete(self):
        response = self.client.post(
            reverse('basket:basket_delete'),
            data={'productId': self.prod_1.id, 'action': 'post'},
            xhr=True)
        self.assertEqual(response.json(), {'basket_price': '80.00', 'basket_qty': 2})
        
        response = self.client.post(
            reverse('basket:basket_delete'),
            data={'productId': self.prod_2.id, 'action': 'post'},
            xhr=True)
        self.assertEqual(response.json(), {'basket_price': '0', 'basket_qty': 0})
    
    def test_basket_delete_bad_request(self):
        response = self.client.post(
            reverse('basket:basket_delete'),
            data={'productId': -1, 'action': 'post'},
            xhr=True)
        self.assertEqual(response.json(), {'status': 'Bad request: product id not found'})
    
    def test_basket_update(self):
        response = self.client.post(
            reverse('basket:basket_update'),
            data={'productId': self.prod_1.id, 'productQty': 3, 'action': 'post'},
            xhr=True)
        self.assertEqual(response.json(), {'basket_qty': 5, 'basket_price': '140.00', 'product_total': '60.00'})
        
        response = self.client.post(
            reverse('basket:basket_update'),
            data={'productId': self.prod_2.id, 'productQty': 1, 'action': 'post'},
            xhr=True)
        self.assertEqual(response.json(), {'basket_qty': 4, 'basket_price': '100.00', 'product_total': '40.00'})
    
    def test_basket_update_bad_request(self):
        response = self.client.post(
            reverse('basket:basket_update'),
            data={'productId': 100, 'productQty': 3, 'action': 'post'},
            xhr=True)
        self.assertEqual(response.json(), {'status': 'Bad request: product id not found'})
