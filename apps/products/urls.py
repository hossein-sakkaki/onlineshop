from django.urls import path
from . import views

app_name= 'products'
urlpatterns = [
    path('cheaper_product/',views.get_cheaper_product, name='cheaper_product'),
    path('newest_product/',views.get_newest_product, name='newest_product'),
    path('popular_product_groups/',views.popular_product_groups, name='popular_product_groups'),
    path('product_detail/<slug:slug>/',views.ProductDetailView.as_view(), name='product_detail'),
]