from basket.basket import Basket


def get_basket(request):
    return {'basket': Basket(request)}
