from importlib import import_module

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.test import Client, TestCase
from django.urls import reverse

from store.models import Category, Product
from store.views import product_all


class TestViewResponses(TestCase):
    
    def setUp(self) -> None:
        self.c = Client()
        user = get_user_model()
        self.user = user.objects.create(user_name='admin')
        self.category = Category.objects.create(name='django', slug='django')
        self.product = Product.objects.create(
            category=self.category,
            title='Django initial',
            created_by=self.user,
            author='admin',
            description='123',
            slug='django-initial',
            price=20.00,
            image='django.png'
        )
    
    def test_url_allowed_hosts(self):
        """
        Test allowed hosts
        :return:
        """
        
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_product_detail_view(self):
        """Test product detail view"""
        self.assertEqual('/product/django-initial/', self.product.get_absolute_url())
        self.assertEqual(reverse('store:product_detail', kwargs={'slug': 'django-initial'}),
                         self.product.get_absolute_url())
        response = self.c.get(reverse('store:product_detail', kwargs={'slug': 'django-initial'}))
        self.assertEqual(response.status_code, 200)
    
    def test_category_view(self):
        """Test category list view"""
        self.assertEqual('/category/django/', self.category.get_absolute_url())
        self.assertEqual(reverse('store:category_list', kwargs={'slug': 'django'}),
                         self.category.get_absolute_url())
        response = self.c.get(reverse('store:category_list', kwargs={'slug': 'django'}))
        self.assertEqual(response.status_code, 200)
    
    def test_homepage_html(self):
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        resource = product_all(request)
        html = resource.content.decode('utf-8')
        self.assertIn('<title>Home</title>', html)
        self.assertEqual(resource.status_code, 200)
