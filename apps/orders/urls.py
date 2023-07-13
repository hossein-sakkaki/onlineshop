from django.urls import path
from . import views

app_name= 'orders'
urlpatterns = [
    path('shop_cart/',views.ShopCartView.as_view(), name='shop_cart'),
 
]