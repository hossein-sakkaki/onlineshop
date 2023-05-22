from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Product, ProductGroup
from django.db.models import Q, Count, Min, Max
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

# Related product
def get_related_product(request, *args, **kwargs):
    current_product = get_object_or_404(Product, slug=kwargs['slug'])
    related_product = []
    for product in current_product.product_group.all():
        related_product.extend(Product.objects.filter(Q(is_active=True), Q(product_group=product), ~Q(id=current_product.id)))
    return render(request, 'products_app/partials/related_product.html', {'related_product':related_product})







# detail product
class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        if product.is_active:
            return render(request, 'products_app/product_detail.html',{'product': product})

# All group of products
class ProductGroupsView(View):
    def get(self, request, *args, **kwargs):
        product_groups = ProductGroup.objects.filter(Q(is_active=True))\
                                        .annotate(count=Count('products_of_groups'))\
                                        .order_by('-count')
        return render(request, 'products_app/product_groups.html', {'product_groups': product_groups})




# def get_product_groups(request):
#     product_groups = ProductGroup.objects.annotate(count = Count('products_of_groups'))\
#                                         .filter(Q(is_active=True), ~Q(count = 0))\
#                                         .order_by('-count')
#     return render(request, 'products_app/partials/product_groups.html', {'product_groups': product_groups})











# All product of list groups
class ProductByGroup(View):
    def get(self, request, *args, **kwargs):
        currrent_group = get_object_or_404(ProductGroup, slug=kwargs['slug'])
        products = Product.objects.filter(Q(is_active=True), Q(product_group=currrent_group))
        return render(request, 'products_app/products_by_group.html', {'products':products, 'currrent_group':currrent_group})
        
    