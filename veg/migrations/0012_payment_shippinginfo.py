# Generated by Django 5.1.3 on 2024-11-25 09:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('veg', '0011_wishlistitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(max_length=50)),
                ('cc_name', models.CharField(max_length=100)),
                ('cc_number', models.CharField(max_length=20)),
                ('cc_expiration', models.CharField(max_length=5)),
                ('cc_cvv', models.CharField(max_length=4)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='veg.order')),
            ],
        ),
        migrations.CreateModel(
            name='ShippingInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.CharField(max_length=255)),
                ('address2', models.CharField(blank=True, max_length=255)),
                ('country', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('zip_code', models.CharField(max_length=20)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='veg.order')),
            ],
        ),
    ]
