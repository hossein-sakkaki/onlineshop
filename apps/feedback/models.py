from django.db import models
from apps.products.models import Product
from apps.accounts.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product", related_name='comments_product')
    commenting_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Comment user", related_name='comments_user1')
    approving_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Comment user", related_name='comments_user2')
    comment_text = models.TextField(verbose_name='Text comment')
    register_date = models.DateTimeField(auto_now_add=True, verbose_name='Register date')
    is_active = models.BooleanField(default=False, verbose_name='Comment status')
    comment_parent = models.ForeignKey("Comment", on_delete=models.CASCADE, null=True, blank=True, verbose_name="Parent comment")
    
    def __str__(self):
        return f'{self.product} {self.commenting_user}'
    
    
    

