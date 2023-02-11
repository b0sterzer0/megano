# Generated by Django 3.2.12 on 2023-02-09 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_settings', '0005_auto_20230111_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='address',
            field=models.CharField(max_length=255, verbose_name='адрес'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='banner_cache_time',
            field=models.PositiveIntegerField(verbose_name='кэш баннеров'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='banner_number',
            field=models.PositiveSmallIntegerField(verbose_name='количество баннеров'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='common_products_top_number',
            field=models.PositiveSmallIntegerField(default=8, verbose_name='количество популярных товаров главной страницы'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='phone_number1',
            field=models.CharField(max_length=255, verbose_name='номер телефона 1'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='phone_number2',
            field=models.CharField(max_length=255, verbose_name='номер телефона 2'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='seller_cache_time',
            field=models.PositiveIntegerField(verbose_name='время кэша продавцов'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='sellers_products_top_cache_time',
            field=models.PositiveIntegerField(verbose_name='время кэша продавцов'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='sellers_products_top_number',
            field=models.PositiveSmallIntegerField(default=8, verbose_name='количество популярных товаров продавца'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='site_name',
            field=models.CharField(max_length=255, verbose_name='название сайта'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='stopping_sales',
            field=models.BooleanField(default=False, verbose_name='остановка продаж'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='total_cache_time',
            field=models.PositiveIntegerField(verbose_name='общий кэш'),
        ),
    ]
