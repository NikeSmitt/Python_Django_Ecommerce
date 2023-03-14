from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404


from basket.basket import Basket
from store.models import Product


def basket_summary(request):
    return render(request, 'basket/summary.html')


def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productId'))
        product_qty = int(request.POST.get('productQty'))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, quantity=product_qty)
        basket_qty = str(len(basket))
        response = JsonResponse({'qty': basket_qty})
        return response


def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productId'))
        try:
            basket.delete(product_id=product_id)
        except KeyError:
            return JsonResponse({'status': 'Bad request: product id not found'})
        basket_qty = len(basket)
        basket_price = str(basket.get_total_price())
        return JsonResponse({'basket_qty': basket_qty, 'basket_price': basket_price})


def basket_update(request):
    """View for update basket product quantity"""
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productId'))
        quantity = int(request.POST.get('productQty'))
        try:
            basket.update(product_id=product_id, quantity=quantity)
        except KeyError:
            return JsonResponse({'status': 'Bad request: product id not found'})
        
        basket_qty = len(basket)
        basket_price = basket.get_total_price()
        product_total = basket.get_product_total(product_id)
        return JsonResponse(
            {'basket_qty': basket_qty, 'basket_price': basket_price, 'product_total': product_total}
        )
    