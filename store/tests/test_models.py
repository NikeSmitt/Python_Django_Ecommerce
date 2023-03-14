from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase

from store.models import Category, Product


class TestCategoryModel(TestCase):
    
    def setUp(self) -> None:
        self.data = Category.objects.create(name='django', slug='django')
    
    def test_category_model_entry(self):
        data = self.data
        self.assertTrue(isinstance(data, Category))
        self.assertTrue(str(data), 'django1')


class TestProductModel(TestCase):
    
    def setUp(self) -> None:
        user = get_user_model()
        self.category = Category.objects.create(name='django', slug='django')
        self.user = user.objects.create(user_name='admin')
        self.product = Product.objects.create(
            category=self.category,
            created_by=self.user,
            title='django essential',
            description='Descr',
            image='django',
            slug='django-course',
            price=20.0,
        )
        
    def test_product_model_entry(self):
        self.assertTrue(str(self.product), 'django essential')
