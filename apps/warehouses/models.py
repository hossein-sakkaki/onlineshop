from django.db import models
from apps.accounts.models import CustomUser
from apps.products.models import Product

class WarehouseType(models.Model):
    warehouse_type_title = models.CharField(max_length=50, verbose_name='Warehouse')
    
    def __str__(self):
        return self.warehouse_type_title
    
class Warehouse(models.Model):
    warehouse_type = models.ForeignKey(WarehouseType, on_delete=models.CASCADE, verbose_name='Warehouse', related_name='warehouses')
    user_registered = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Costom User', related_name='warehouseuser_registered')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product', related_name='warehouses_products')
    qty = models.IntegerField(verbose_name="Quantity")
    price = models.IntegerField(verbose_name='Unit price', null=True, blank=True)
    register_date = models.DateTimeField(auto_now_add=True, verbose_name='Register date')
    
    def __str__(self):
        return f'{self.warehouse_type} - {self.product}'
    
    
