from django.shortcuts import render, get_object_or_404

from .models import Category, Product


def all_products(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    context = {
        'product': product,
    }
    return render(request, 'store/products/detail.html', context)


def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(in_stock=True)
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'store/products/category.html', context)
