from django.shortcuts import render
from django.views import View
from .shop_cart import ShopCart

class ShopCartView(View):
    def get(self, request, *args, **kwargs):
        shop_cart = ShopCart(request)
        return render(request, 'order_app/shop_cart.html', {'shop_cart': shop_cart})
    
def add_to_shop_cart(request):
    pass
        
