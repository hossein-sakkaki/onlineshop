from django.db import models
from utils import FileUpload
from django.utils import timezone
from django.utils.html import mark_safe

class Slider(models.Model):
    slider_title_1 = models.CharField(max_length=500, null=True, blank=True, verbose_name="Title 1")
    slider_title_2 = models.CharField(max_length=500, null=True, blank=True, verbose_name="Title 2")
    slider_title_3 = models.CharField(max_length=500, null=True, blank=True, verbose_name="Title 3")
    file_upload = FileUpload('images','slider')
    image_name = models.ImageField(upload_to=file_upload.upload_to, verbose_name="Slider Image")
    slider_link = models.URLField(max_length=200, null=True, blank=True, verbose_name="Slider Link")
    is_active = models.BooleanField(default=True, blank=True, verbose_name="Active/Inactive")
    register_date = models.DateTimeField(auto_now_add=True, verbose_name="Register Date")
    published_date = models.DateTimeField(default=timezone.now, verbose_name="Published Date")
    update_date = models.DateTimeField(auto_now=True, verbose_name="Update Date")
    
    def __str__(self) -> str:
        return f'slider_title_1'
    
    def image_slide(self):
        return mark_safe(f'<img src="/media/{self.image_name}" style="width: 80px; height: 50px;" />')


    def link(self):
        return mark_safe(f'<a href="{self.slider_link}" target="_blank">Link</a>')
