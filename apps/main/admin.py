from django.contrib import admin
from .models import Slider

@admin.register(Slider)
class AdminSlider(admin.ModelAdmin):
    list_display = ('slider_title_1','slider_title_2','slider_title_3','link','is_active','register_date')
    list_filter = ('slider_title_1',)
    search_fields = ('slider_title_1',)
    ordering = ('update_date',)
    readonly_fields = ('image_slide',) 

