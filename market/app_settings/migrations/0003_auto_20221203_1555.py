# Generated by Django 3.2.12 on 2022-12-03 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_settings', '0002_data_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='common_products_top_number',
            field=models.PositiveSmallIntegerField(default=8, verbose_name='Количество популярных товаров главной страницы'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='seller_cache_time',
            field=models.PositiveIntegerField(default=1, verbose_name='Время кэша продавцов'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='sellers_products_top_cache_time',
            field=models.PositiveIntegerField(default=1, verbose_name='Время кэша продавцов'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='sellers_products_top_number',
            field=models.PositiveSmallIntegerField(default=8, verbose_name='Количество популярных товаров продавца'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='banner_cache_time',
            field=models.PositiveIntegerField(verbose_name='Время кэша баннеров'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='total_cache_time',
            field=models.PositiveIntegerField(verbose_name='Время общего кэша'),
        ),
    ]
