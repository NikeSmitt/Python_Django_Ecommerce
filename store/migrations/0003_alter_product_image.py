# Generated by Django 4.1.7 on 2023-03-06 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_rename_in_active_product_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='defaults/default_book_img.png', upload_to='images/'),
        ),
    ]