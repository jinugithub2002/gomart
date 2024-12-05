# Generated by Django 5.1.3 on 2024-11-28 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('veg', '0013_delete_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Delivered', 'Delivered')], default='Pending', max_length=20),
        ),
    ]
