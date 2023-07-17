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
    path('product_groups_partials/', views.get_product_groups, name='product_groups_partials'),
    
    path('compare_table/',views.compare_table, name='compare_table'),
    path('add_to_compare_list/',views.add_to_compare_list, name='add_to_compare_list'),
    path('delete_from_compare_list/',views.delete_from_compare_list, name='delete_from_compare_list'),
    path('status_of_compare_list/',views.status_of_compare_list, name='status_of_compare_list'),
]