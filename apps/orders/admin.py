from django.contrib import admin
from .models import OrderState, Order, OrderDetail

@admin.register(OrderState)
class AsminOrderState(admin.ModelAdmin):
    list_display = ('id','order_state_title')
    
class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    extra = 3
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'register_date','is_finaly','discount')
    inlines = [OrderDetailInline]
