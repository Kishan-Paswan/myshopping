# Generated by Django 4.2.7 on 2023-11-25 06:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0005_remove_cart_product_title_remove_cart_products_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Cart',
        ),
    ]
