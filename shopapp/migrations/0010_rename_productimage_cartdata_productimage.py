# Generated by Django 4.2.7 on 2023-11-25 07:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0009_cartdata_productimage_cartdata_productname_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartdata',
            old_name='productImage',
            new_name='productimage',
        ),
    ]