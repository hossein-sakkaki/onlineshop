from django.db import models
from django.utils import timezone
from apps.accounts.models import Customer
from apps.products.models import Product
import uuid


class OrderState(models.Model):
    order_state_title = models.CharField(max_length=30, verbose_name='Order title state')
    
    def __str__(self):
        return self.order_state_title
    
class PaymentType(models.Model):
    payment_title = models.CharField(max_length=50, verbose_name='Payment title')
    
    def __str__(self) -> str:
        return self.payment_title
    
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,related_name='orders' ,verbose_name='Costomer')
    register_date = models.DateField(default=timezone.now, verbose_name='Register date')
    update_date = models.DateField(auto_now=True, verbose_name='Edit finaly date')
    is_finaly = models.BooleanField(default=False, verbose_name='Finaly')
    order_code = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name='Create code for order')
    discount = models.IntegerField(blank=True, null=True, default=None, verbose_name='Discount on invoice')
    description = models.TextField(null=True, blank=True, verbose_name='Description')
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE, default=None, null=True, blank=True, verbose_name="Payment title", related_name='payment_types')
    
    order_state = models.ForeignKey(OrderState, on_delete=models.CASCADE, related_name='orders_states',verbose_name="Order state", null=True, blank=True)
    

    
    def get_order_total_price(request):
        sum = 0
        

class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="order", related_name='orders_details1')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="product", related_name='orders_details2')
    qty = models.PositiveIntegerField(default=1, verbose_name='Quantity')
    price = models.IntegerField(verbose_name='Price in the invoice')
    
    def __str__(self):
        return f"{self.order}\t{self.product}\t{self.qty}\t{self.price}" 
    