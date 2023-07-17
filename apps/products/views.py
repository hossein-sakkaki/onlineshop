from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views import View
from .models import Product, ProductGroup, Brand
from django.db.models import Q, Count, Min, Max
from .compare import CompareProduct
from django.core.paginator import Paginator
# Create your views here.

def get_root_group():
    return ProductGroup.objects.filter(Q(is_active=True) & Q(group_parent=None))


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

# product group list for filter
def get_product_groups(request):
    product_groups = ProductGroup.objects.annotate(count = Count('products_of_groups'))\
                                        .filter(Q(is_active=True), ~Q(count = 0))\
                                        .order_by('-count')
    return render(request, 'products_app/partials/product_groups.html', {'product_groups': product_groups})

# brands list for filter
def get_brands(request, *args, **kwargs):
    product_group = get_object_or_404(ProductGroup, slug=kwargs['slug'])
    brand_list_id = product_group.products_of_groups.filter(is_active = True).values('brand_id')
    brand = Brand.objects.filter(pk__in=brand_list_id)\
                                .annotate(count = Count('products_of_brands'))\
                                .filter(~Q(count=0))\
                                .order_by('-count')
    return render(request, 'product_app/partials/brands.html', {'brand': brand})

def get_features_for_filter(request, *args, **kwargs):
    product_group = get_object_or_404(ProductGroup, slug=kwargs['slug'])
    feature_list = product_group.features_of_groups.all()
    feature_dict = dict()
    for feature in feature_list:
        feature_dict[feature] = feature.feature_values.all()
        
    return render(request, 'product_app/partials/features_filter.html', {'feature_dict': feature_dict})


    


class ProductsByGroupsView(View):
    def get(self, request, *args, **kwargs):
        slug = kwargs['slug']
        current_group = get_object_or_404(ProductGroup, slug=slug)
        products = Product.objects.filter(Q(is_active=True) & Q(product_group=current_group))
        
        res_aggr = products.aggregate(min=Min('price'), max=Max('price'))
        
        # price filter
        filter = ProductFilter(request.GET, queryset=products)
        products = filter.qs
        
        # brand filter
        brands_filter = request.GET.getlist('brand')
        if brands_filter:
            products = products.filter(brand__id__in = brands_filter)
            
        # features filter
        features_filter = request.GET.getlist('features')
        if features_filter:
            products = products.filter(product_feature__filter_value__id__in=features_filter).discard()
            
        sort_type = request.GET.get('sort_type')
        if not sort_type:
            sort_type = '0'

        if sort_type == '1':
            products = products.order_by('price')
            
        if sort_type == '2':
            products = products.order_by('-price')
            
        group_slug = slug
        product_per_page = 3
        paginator = Paginator(products, product_per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        product_count = products.count()
        
        show_count_product = []
        i = product_per_page
        while i < product_count:
            show_count_product.append(i)
            i *= 2
        show_count_product.append(i)
        
        context = {
            'products': products,
            'current_group': current_group,
            'res_aggr': res_aggr,
            'group_slug': group_slug,
            'page_obj': page_obj,
            'product_count': product_count,
            'show_count_product': show_count_product,
            'filter': filter,
            'sort_type': sort_type
        }
        return render(request, 'products_app/products_by_group.html', context)
        

            
        
            


# All product of list groups
class ProductByGroup(View):
    def get(self, request, *args, **kwargs):
        currrent_group = get_object_or_404(ProductGroup, slug=kwargs['slug'])
        products = Product.objects.filter(Q(is_active=True), Q(product_group=currrent_group))
        return render(request, 'products_app/products_by_group.html', {'products':products, 'currrent_group':currrent_group})
        
class ShowCompareListView(View):
    def get(self, request, *args, **kwargs):
        compare_list = CompareProduct(request)
        context = {
            'compare_list': compare_list,
        }
        return render(request, 'product_app/compare_list.html', context)
    
def compare_table(request):
    compare_list = CompareProduct(request)
    
    products = []
    for productId in compare_list.compare_product:
        product = Product.objects.get(id = productId)
        products.append(product)
        
    features = []
    for product in products:
        for item in product.product_features.all():
            if item.feature not in features:
                features.append(item.feature)
    
    context = {
        'products': products,
        'features': features
    }
    return render(request, 'product_app/partials/compare_table.html', context)
   

def status_of_compare_list(request):
    compareList = CompareProduct(request)
    return HttpResponse(compareList.count)
             
def add_to_compare_list(request):
    productId = request.GET.get('productId')
    # productGroupId = request.GET.get('productGroupId')
    compareList = CompareProduct(request)
    compareList.add_to_compare_product(productId)
    return HttpResponse('Add Product To List')
    
def delete_from_compare_list(request):
    productId = request.GET.get('productId')
    compareList = CompareProduct(request)
    compareList.delete_from_compare_product(productId)
    return redirect('products:compare_table')