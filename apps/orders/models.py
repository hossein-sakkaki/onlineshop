from django.db import models
from django.utils import timezone
from apps.accounts.models import Customer


class OrderState(models.Model):
    order_state_title = models.CharField(max_length=30, verbose_name='Order title state')
    
    def __str__(self):
        return self.order_state_title
    
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,related_name='orders' ,verbose_name='Costomer')
    register_date = models.DateField(default=timezone.now, verbose_name='Register date')
    update_date = models.DateField(auto_now=True, verbose_name='Edit finaly date')
    is_finaly = models.BooleanField(default=False, verbose_name='Finaly')
    
    order_state = models.ForeignKey(OrderState, on_delete=models.CASCADE, related_name='orders_states',verbose_name="Order state", null=True, blank=True)
    

    
    def get_order_total_price(request):
        sum = 0
        