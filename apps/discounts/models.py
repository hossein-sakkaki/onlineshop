from django.db import models
from apps.products.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator

class Coupon (models.Model):
    coupon_code = models.CharField(max_length=10, unique=True)
    start_date = models.DateField(verbose_name='Start date')
    end_date = models.DateField(verbose_name='End date')
    discount = models.IntegerField(verbose_name='Discount', validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField(default=False, verbose_name='Status')
    
    def __str__(self):
        return self.coupon_code


class DiscountBasket(models.Model):
    discount_title = models.CharField(max_length=100, verbose_name='Discount basket title')
    start_date = models.DateField(verbose_name='Start date')
    end_date = models.DateField(verbose_name='End date')
    discount = models.IntegerField(verbose_name='Discount', validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField(default=False, verbose_name='Status')
    
    def __str__(self):
        return self.discount_title
    
class DiscountBasketDetails(models.Model):
    discount_basket = models.ForeignKey(DiscountBasket, on_delete=models.CASCADE, verbose_name="Discount basket", related_name='discount_basket_details1')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product', related_name='discount_basket_details2')
    