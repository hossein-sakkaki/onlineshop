from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.http import HttpResponse
from django.core import serializers
from .models import Brand, ProductGroup, Feature, Product, ProductFeature, ProductGallery
from django.db.models.aggregates import Count
from django_admin_listfilter_dropdown.filters import DropdownFilter


#---------==========================================================---------#
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_title','slug')
    list_filter = ('brand_title',)
    search_fields = ('brand_title',)
    ordering = ('brand_title',)
    
    prepopulated_fields = {'slug':('brand_title',)}
    
#---------==========================================================---------#
# Actions for product group admin #
def deactive_product_group(modeladmin, request, queryset):
    qs = queryset.update(is_active=False)
    message = ''
    if qs == 1:
        message = f'{qs} item has been deactivated'
    elif qs > 1:
        message = f'{qs} items were deactivated'
    modeladmin.message_user(request,message)

def active_product_group(modeladmin, request, queryset):
    qs = queryset.update(is_active=True)
    message = ''
    if qs == 1:
        message = f'{qs} item has been Activated'
    elif qs > 1:
        message = f'{qs} items were Activated'
    modeladmin.message_user(request,message)
    
def export_json(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/json')
    serializers.serialize('json', queryset, stream=response)
    return response

# inline view product group admin #
class ProductGroupInstanceInlineAdmin(admin.TabularInline):
    model = ProductGroup
    
@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display = ('group_title','is_active','group_parent','slug','register_date','update_date','count_sub_group')
    list_filter = ('group_title',('group_parent',DropdownFilter))
    search_fields = ('group_title',)
    ordering = ('group_parent','group_title')
    prepopulated_fields = {'slug':('group_title','group_parent')}

    inlines = [ProductGroupInstanceInlineAdmin]
    actions = [deactive_product_group, active_product_group, export_json]
    
    def get_queryset(self, *args, **kwargs):
        qs = super(ProductGroupAdmin,self).get_queryset(*args, **kwargs)
        qs = qs.annotate(sub_group=Count('groups'))
        return qs
    
    def count_sub_group(self, obj):
        return obj.sub_group
    
    # count_sub_group.short_description = 'Count Sub Group'

     