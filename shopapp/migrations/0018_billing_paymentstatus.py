# Generated by Django 4.2.7 on 2023-12-06 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0017_billing_paymentmode'),
    ]

    operations = [
        migrations.AddField(
            model_name='billing',
            name='paymentStatus',
            field=models.BooleanField(default=False),
        ),
    ]
