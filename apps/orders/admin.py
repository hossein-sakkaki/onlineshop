from django.contrib import admin
from .models import OrderState

@admin.register(OrderState)
class AsminOrderState(admin.ModelAdmin):
    list_display = ('id','order_state_title')
