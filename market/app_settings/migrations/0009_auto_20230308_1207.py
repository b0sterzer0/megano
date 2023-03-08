# Generated by Django 3.2.12 on 2023-03-08 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_settings', '0008_auto_20230308_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='express_delivery_cost',
            field=models.PositiveIntegerField(verbose_name='стоимость экспресс доставки'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='min_amount_for_free_delivery',
            field=models.PositiveIntegerField(verbose_name='минимальная сумма для бесплатной обычной доставки'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='ordinary_delivery_cost',
            field=models.PositiveIntegerField(verbose_name='стоимость обычной доставки'),
        ),
    ]
