from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import CommentForm
from apps.products.models import Product
from .models import Comment
from django.contrib import messages

class CommentView(View):
    def get(self, requset, *args, **kwargs):
        produst_id = requset.GET.get['productId']
        comment_id = requset.GET.get['cpmmentId']
        slug = kwargs['slug']
        initial_dict = {
            'produst_id': produst_id,
            'comment_id': comment_id
        }
        form = CommentForm(initial=initial_dict)
        return render(requset,'',{'form':form, 'slug': slug})
    
    def post(self, request, *args, **kwargs):
        slug = kwargs['slug']
        form = CommentForm(request.POST)
        if form.is_valid:
            data = form.cleaned_data
            product = get_object_or_404(Product, slug= slug)
            parent = None
            if (data['comment_id']):
                parent_id = data['comment_id']
                parent = Comment.objects.get(id=parent_id)
            Comment.objects.create(
                product = product,
                commenting_user = request.user,
                comment_text = data['comment_text'],
                comment_parent = parent
            )
            messages.success(request, 'Your message submit','success')
            return redirect('products:product_detail', product.slug)
        messages.error(request, 'Send error','danger')
        return redirect('products:product_detail', product.slug)

            