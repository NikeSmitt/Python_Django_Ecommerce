from django.urls import path

from .views import category_list, product_all, product_detail

app_name = 'store'

urlpatterns = [
    path('', product_all, name='product_all'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('category/<slug:slug>/', category_list, name='category_list'),
]
