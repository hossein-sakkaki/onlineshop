# Generated by Django 4.1.3 on 2023-07-02 05:40

from django.db import migrations, models
import utils


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_brand_image_name_alter_product_image_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='image_name',
            field=models.ImageField(upload_to=utils.FileUpload.upload_to, verbose_name='Product group picture'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image_name',
            field=models.ImageField(upload_to=utils.FileUpload.upload_to, verbose_name='Product picture'),
        ),
        migrations.AlterField(
            model_name='productgallery',
            name='image_name',
            field=models.ImageField(upload_to=utils.FileUpload.upload_to, verbose_name='Product group picture'),
        ),
        migrations.AlterField(
            model_name='productgroup',
            name='image_name',
            field=models.ImageField(upload_to=utils.FileUpload.upload_to, verbose_name='Product group picture'),
        ),
    ]
