from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Product, ProductGroup
from django.db.models import Q, Count
# Create your views here.



def get_root_group():
    return ProductGroup.objects.filter(Q(is_active=True), Q(group_parent=None))



# Cheapest product
def get_cheaper_product(request, *args, **kwargs):
    products = Product.objects.filter(is_active=True).order_by('price')[:5]
    product_group = get_root_group()
    context = {
        'products':products,
        'product_group': product_group
    }
    return render(request, 'products_app/partials/cheaper_product.html', context)

# Newest product
def get_newest_product(request, *args, **kwargs):
    products = Product.objects.filter(is_active=True).order_by('-published_date')[:5]
    product_group = get_root_group()
    context = {
        'products':products,
        'product_group': product_group
    }
    return render(request, 'products_app/partials/newest_product.html', context)

# Popular product groups
def popular_product_groups(request, *args, **kwargs):
    product_group = ProductGroup.objects.filter(Q(is_active=True))\
                                        .annotate(count=Count('products_of_groups'))\
                                        .order_by('-count')[:6]
    context = {
        'product_group': product_group,
    }
    return render(request,'products_app/partials/popular_product_groups.html', context)

# detail product
class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        if product.is_active:
            return render(request, 'products_app/product_detail.html',{'product': product})