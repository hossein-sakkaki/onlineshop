from django.db import models
from django.db.models import Sum, Avg
from utils import FileUpload
from django.utils import timezone
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from middlewares.middlewares import RequestMiddleware

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
    summery_description = models.TextField(default="", blank=True, null=True)
    description = RichTextUploadingField(config_name='default', blank=True, null=True, verbose_name='Product description')
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
    
    def get_quantity_in_warehouse(self):
        sum1 = self.warehouses_products.flter(warehouse_type_id=1).aggregate(sum('qty'))
        sum2 = self.warehouses_products.flter(warehouse_type_id=2).aggregate(sum('qty'))
        input = 0
        if sum1['qty__sum'] != None:
            input = sum1['qty__sum']
        output = 0
        if sum2['qty__sum'] != None:
            input = sum2['qty__sum']
        return input - output
    
    def get_user_score(self):
        request = RequestMiddleware(get_response = None)
        request = request.thread_local.current_request
        score = 0
        user_score = self.scoring_product.filter(scoring_user=request.user)
        if user_score.count()>0:
            score = user_score[0].score
        return score
    
    def get_average_score(self):
        avgScore = self.scoring_product.all().aggregate(Avg('score'))['score__avg']
        if avgScore == None:
            avgScore = 0
        return int(avgScore)
    
    def get_user_favorite(self):
        request = RequestMiddleware(get_response = None)
        request = request.thread_local.current_request
        flag = self.favorite_product.filter(favorite_user=request.user)
        return flag
    
    def getMainProductGroups(self):
        return self.product_group.all()[0].id
        
            
    def __str__(self) -> str:
        return self.product_name
    
    def get_absolute_url(self):
        return reverse("products:product_detail", kwargs={"slug": self.slug})
    
#---------==========================================================---------#
class FeatureValue(models.Model):
    value_title = models.CharField( max_length=100, verbose_name="Value title")
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, verbose_name="Feature", related_name="feature_values")
    
    def __str__(self):
        return f'{self.id} {self.value_title}'

#---------==========================================================---------#
class ProductFeature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product", related_name="product_features")
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, verbose_name="Feature")
    value = models.CharField(max_length=100, verbose_name="Product feature value")
    feature_value = models.ForeignKey(FeatureValue, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Feature value", related_name="product_group")
    
    def __str__(self) -> str:
        return f"{self.product}-{self.feature}: {self.value}"

#---------==========================================================---------#
class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product", related_name="gallery_images")
    file_upload = FileUpload('images', 'product_gallery')
    image_name = models.ImageField(upload_to=file_upload.upload_to, verbose_name="Product group picture")