from django.db import models
from utils import FileUpload
from django.utils import timezone

#---------==========================================================---------#

# Create your models here.
class Brand(models.Model):
    brand_title = models.CharField(max_length=100, verbose_name="Brand name")
    file_upload = FileUpload('images', 'brand')
    image_name = models.ImageField(upload_to=file_upload.upload_to, verbose_name="Product group picture")
    slug = models.SlugField(max_length=200, null=True)
    
    def __str__(self) -> str:
        return self.brand_title
    
#---------==========================================================---------#
class ProductGroup(models.Model):
    group_title = models.CharField(max_length=100, verbose_name="Product group title")
    file_upload = FileUpload('images', 'product_group')
    image_name = models.ImageField(upload_to=file_upload.upload_to, verbose_name="Product group picture")
    description = models.TextField(blank=True, verbose_name='Product group description')
    group_parent = models.ForeignKey('ProductGroup', on_delete=models.CASCADE, verbose_name="Parent product group", related_name='groups', null=True, blank=True)
    
    is_active = models.BooleanField(default=True, blank=True, verbose_name="Active/Deactive")
    slug = models.SlugField(max_length=200, null=True)
    
    register_date = models.DateTimeField(auto_now=True, verbose_name="Register date")
    published_date = models.DateTimeField(default=timezone.now, verbose_name="Published date")
    update_date = models.DateTimeField(auto_now=True, verbose_name="Update date")
    
    def __str__(self) -> str:
        return self.group_title
    
#---------==========================================================---------#
class Feature(models.Model):
    feature_name = models.CharField(max_length=100, verbose_name="Feature name")
    product_group = models.ManyToManyField(ProductGroup, verbose_name="Product group", related_name="feature_of_groups")
    
    def __str__(self) :
        return self.feature_name
    
#---------==========================================================---------#
class Product(models.Model):
    product_name = models.CharField(max_length=200, verbose_name="Product name")
    description = models.TextField(blank=True, null=True, verbose_name='Product description')
    file_upload = FileUpload('images', 'product')
    image_name = models.ImageField(upload_to=file_upload.upload_to, verbose_name="Product picture")
    price = models.PositiveIntegerField(default=0, verbose_name="Product price")
    
    product_group = models.ManyToManyField(ProductGroup, verbose_name="Product group", related_name="products_of_groups")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name="Product brand", null=True, related_name='brands')
    feature = models.ManyToManyField(Feature, through="ProductFeature")
    
    is_active = models.BooleanField(default=True, blank=True, verbose_name="Active/Deactive")
    slug = models.SlugField(max_length=200, null=True)
    
    register_date = models.DateTimeField(auto_now=True, verbose_name="Register date")
    published_date = models.DateTimeField(default=timezone.now, verbose_name="Published date")
    update_date = models.DateTimeField(auto_now=True, verbose_name="Update date")
    
    
    def __str__(self) -> str:
        return self.product_name
    
#---------==========================================================---------#
class ProductFeature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product")
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, verbose_name="Feature")
    value = models.CharField(max_length=100, verbose_name="Product feature value")
    
    def __str__(self) -> str:
        return f"{self.product}-{self.feature}: {self.value}"

#---------==========================================================---------#
class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product")
    file_upload = FileUpload('images', 'product_gallery')
    image_name = models.ImageField(upload_to=file_upload.upload_to, verbose_name="Product group picture")