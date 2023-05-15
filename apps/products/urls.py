from django.urls import path
from . import views

app_name= 'products'
urlpatterns = [
    path('cheaper_product/',views.get_cheaper_product, name='cheaper_product'),
    path('newest_product/',views.get_newest_product, name='newest_product'),
    path('popular_product_groups/',views.popular_product_groups, name='popular_product_groups'),
    path('related_product/<slug:slug>/',views.get_related_product, name='related_product'),
    path('product_detail/<slug:slug>/',views.ProductDetailView.as_view(), name='product_detail'),
    path('product_groups/',views.ProductGroupsView.as_view(), name='product_groups'),
    path('product_by_groups/<slug:slug>/',views.ProductByGroup.as_view(), name='product_by_groups'),
]