from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .shop_cart import ShopCart
from apps.products.models import Product
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.accounts.models import Customer
from apps.orders.models import Order, OrderDetails

class ShopCartView(View):
    def get(self, request, *args, **kwargs):
        shop_cart = ShopCart(request)
        return render(request, 'order_app/shop_cart.html', {'shop_cart': shop_cart})

def show_shop_cart(request):
    shop_cart = ShopCart(request)
    total_price = shop_cart.calc_total_price()
    delivery = 20
    if total_price > 500:
        delivery = 0
    tax = 0.09 * total_price
    order_final_price = total_price + delivery + tax
    context = {
        'shop_cart': shop_cart,
        'shop_cart_count': shop_cart.count,
        'total_price': total_price,
        'delivery': delivery,
        'tax': tax,
        'order_final_price': order_final_price
    }
    return render(request, 'order_app/partials/show_shop_cart.html', context)
    

def add_to_shop_cart(request):
    product_id = request.GET.get('product_id')
    qty = request.GET.get('qty')
    shop_cart = ShopCart(request)
    product = get_object_or_404(Product, id=product_id)
    shop_cart.add_to_shop_cart(product, qty)
    return HttpResponse(shop_cart.count)

def delete_from_shop_cart(request):
    product_id = request.GET.get('product_id')
    product = get_object_or_404(Product, id=product_id)
    shop_cart = ShopCart(request)
    shop_cart.delete_from_shop_cart(product)
    return redirect('orders:show_shop_cart')

def update_shop_cart(request):
    product_id_list = request.GET.getlist('product_id_list[]')
    qty_list = request.GET.getlist('qty_list[]')
    shop_cart = ShopCart(request)
    shop_cart.update(product_id_list,qty_list)
    return redirect('orders:show_shop_cart')
    
def status_of_shop_cart(request):
    shop_cart = ShopCart(request)
    return HttpResponse(shop_cart.count)


class CreateOrderView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        customer = get_object_or_404(customer, user=request.user)
        if not customer:
            customer = Customer.objects.create(user=request.user)
            
            order = Order.objects.create(customer=customer)
            shop_cart = ShopCart(request)
            for item in shop_cart:
                OrderDetails.objects.create(
                    order = order,
                    product = item['product'],
                    price = item['price'],
                    qty = item['qty']
                )
            return redirect('main:index')