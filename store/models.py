from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()

class CreateUpdateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Category(CreateUpdateMixin):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    
    def get_absolute_url(self):
        return reverse('store:category_list', kwargs={'slug': self.slug})
    
    class Meta:
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name


class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(in_stock=True)


class Product(CreateUpdateMixin):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100, default='admin')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', default='defaults/default_book_img.png')
    slug = models.SlugField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    objects = models.Manager()
    products = ProductManager()
    
    class Meta:
        ordering = ('-created_at',)
    
    def get_absolute_url(self):
        return reverse('store:product_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.title
