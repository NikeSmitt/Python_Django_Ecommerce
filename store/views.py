from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def product_all(request):
    products = Product.objects.prefetch_related('product_image').filter(is_active=True)
    return render(request, 'store/home.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    context = {
        'product': product,
    }
    return render(request, 'store/products/detail.html', context)


def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(
        category__in=category.get_descendants(include_self=True)).filter(is_active=True)
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'store/products/category.html', context)
