from django.shortcuts import render
from django.views import View
from apps.products.models import Product
from django.db.models import Q

class SearchResultView(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        products = Product.objects.filter(Q(product_name__icontains=query))
        return render(request,'search_app/search_results.html', {'products': products})
        
        
