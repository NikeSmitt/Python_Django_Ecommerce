from decimal import Decimal

from store.models import Product


class Basket:
    """
    class for utilize basket
    """
    
    DELIVERY_COST = Decimal(11.50)
    
    def __init__(self, request):
        self.session = request.session
        self.basket = self.session.setdefault('basket', {})
    
    def add(self, product: Product, quantity: int):
        """
        Adding and updating users basket session data
        """
        
        # ------------------- всегда!! всегда делай так ---------------------------------#
        product_id = str(product.id)
        ####################################################################################
        
        if product_id not in self.basket:
            self.basket[product_id] = {'quantity': quantity, 'price': str(product.regular_price)}
        else:
            new_quantity = int(self.basket[product_id]['quantity']) + quantity
            self.basket[product_id]['quantity'] = new_quantity
        
        self.save()
    
    def delete(self, product_id: int):
        """Delete product from the basket"""
        del self.basket[str(product_id)]
        self.save()
    
    def update(self, product_id: int, quantity: int):
        """Update product quantity in basket"""
        self.basket[str(product_id)]['quantity'] = str(quantity)
        self.save()
    
    def __len__(self):
        return sum(int(item['quantity']) for item in self.basket.values())
    
    def save(self):
        """Save session"""
        self.session.modified = True
    
    def get_total_price(self):
        """Getting total basket price"""
        total_price = sum([Decimal(item['price']) * int(item['quantity']) for item in self.basket.values()])
        return total_price
    
    def get_total_price_with_delivery(self):
        return self.DELIVERY_COST + self.get_total_price()
    
    def get_product_total(self, product_id: int):
        """Get total product price in basket"""
        product = self.basket[str(product_id)]
        price = Decimal(product['price'])
        quantity = int(product['quantity'])
        return price * quantity
    
    def __iter__(self):
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()
        for product in products:
            basket[str(product.id)]['product'] = product
        
        for item in basket.values():
            item['total_price'] = item['product'].regular_price * int(item['quantity'])
            
            yield item
