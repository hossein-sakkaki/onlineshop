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
    
    
class Scoring(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product", related_name='scoring_product')
    scoring_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Scoring user", related_name='scoring_user1')
    register_date = models.DateTimeField(auto_now_add=True, verbose_name='Register date')
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name='Score')
    
    def __str__(self):
        return f'{self.product} {self.scoring_user}'
    
class Favorite(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product", related_name='favorite_product')
    favorite_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Favorite user", related_name='favorite_user1')
    register_date = models.DateTimeField(auto_now_add=True, verbose_name='Register date')
    
    def __str__(self):
        return f'{self.product} {self.favorite_user}'
    
    


    
    
    
    

