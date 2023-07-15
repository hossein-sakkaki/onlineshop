from django.dispatch import receiver
from django.db.models.signals import post_delete
from .models import Product
from django.conf import Settings
import os

@receiver(post_delete, sender=post_delete)
def delete_product_image(sender, **kwargs):
    path = Settings.MEDIA_RRT+str(kwargs['instance'].image_name)
    if os.path.isfile(path):
        os.remove(path)