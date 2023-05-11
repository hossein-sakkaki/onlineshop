from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.http import HttpResponse
from django.core import serializers
from .models import Brand, ProductGroup, Feature, Product, ProductFeature, ProductGallery
from django.db.models.aggregates import Count
from django_admin_listfilter_dropdown.filters import DropdownFilter
from django.db.models import Q

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
        message = f'{qs} product group has been deactivated'
    elif qs > 1:
        message = f'{qs} product groups were deactivated'
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
    
#---------==========================================================---------#
@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('feature_name',)
    list_filter = ('feature_name',)
    search_fields = ('feature_name',)
    ordering = ('feature_name',)
    
#---------==========================================================---------#
# Actions for product group admin #
def deactive_product(modeladmin, request, queryset):
    qs = queryset.update(is_active=False)
    message = ''
    if qs == 1:
        message = f'{qs} product has been deactivated'
    elif qs > 1:
        message = f'{qs} products were deactivated'
    modeladmin.message_user(request,message)

def active_product(modeladmin, request, queryset):
    qs = queryset.update(is_active=True)
    message = ''
    if qs == 1:
        message = f'{qs} item has been Activated'
    elif qs > 1:
        message = f'{qs} items were Activated'
    modeladmin.message_user(request,message)

# inline view product admin #
class ProductFeatureInlineAdmin(admin.TabularInline):
    model = ProductFeature
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','display_product_group','price','brand','is_active','update_date','slug')
    list_filter = ('brand','product_group')
    search_fields = ('product_name',)
    ordering = ('update_date','product_name')
    prepopulated_fields = {'slug':('product_name','brand')}
    
    actions = [deactive_product, active_product]
    inlines = [ProductFeatureInlineAdmin]

    def display_product_group(self, obj):
        return ', '.join([group.group_title for group in obj.product_group.all()])

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'product_group':
            kwargs['queryset'] = ProductGroup.objects.filter(~Q(group_parent=None))
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    
    fieldsets = (
        ('Product information', {
            "fields": (
                'product_name',
                'product_group',
                ('image_name','brand','is_active'),
                'description',
                'slug'
            ),
        }),
        ('Date & Time', {
            "fields": (
                'published_date',
            ),
        }),
    )
    
    
    
    
#---------==========================================================---------#
