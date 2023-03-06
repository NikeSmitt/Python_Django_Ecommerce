from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


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


class Product(CreateUpdateMixin):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100, default='admin')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/')
    slug = models.SlugField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created_at',)

    def get_absolute_url(self):
        return reverse('store:product_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title
