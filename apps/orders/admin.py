from django.contrib import admin
from .models import OrderState, Order, OrderDetails

@admin.register(OrderState)
class AsminOrderState(admin.ModelAdmin):
    list_display = ('id','order_state_title')
    
class OrderDetailInline(admin.TabularInline):
    model = OrderDetails
    extra = 3
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'register_date','is_finaly','discount')
    inlines = [OrderDetailInline]
