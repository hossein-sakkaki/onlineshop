from django.urls import path
from . import views

app_name= 'orders'
urlpatterns = [
    path('shop_cart/',views.ShopCartView.as_view(), name='shop_cart'),
    path('add_to_shop_cart/',views.add_to_shop_cart, name='add_to_shop_cart'),
 
]