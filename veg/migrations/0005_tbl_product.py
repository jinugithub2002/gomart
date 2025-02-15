# Generated by Django 5.1.3 on 2024-11-19 09:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('veg', '0004_tbl_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='tbl_product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_image', models.ImageField(blank=True, null=True, upload_to='media')),
                ('product_code', models.CharField(max_length=100, null=True)),
                ('product_name', models.CharField(max_length=100, null=True)),
                ('product_price', models.CharField(max_length=100, null=True)),
                ('total', models.FloatField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('opening_stock', models.IntegerField()),
                ('closing_stock', models.IntegerField()),
                ('status', models.BooleanField(default=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='veg.tbl_brands')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='veg.tbl_category')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='veg.tbl_country')),
            ],
        ),
    ]
