# Generated by Django 5.1.2 on 2024-11-26 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_product_colors_product_sizes'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='size',
            field=models.CharField(default='None', max_length=10),
        ),
    ]
