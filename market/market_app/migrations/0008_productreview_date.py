# Generated by Django 3.2.12 on 2023-02-11 17:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('market_app', '0007_alter_sellerproduct_seller'),
    ]

    operations = [
        migrations.AddField(
            model_name='productreview',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='дата'),
            preserve_default=False,
        ),
    ]
