# Generated by Django 3.2.12 on 2022-10-14 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=255, verbose_name='Название сайта')),
                ('phone_number1', models.CharField(max_length=255, verbose_name='Номер телефона 1')),
                ('phone_number2', models.CharField(max_length=255, verbose_name='Номер телефона 2')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес')),
                ('banner_number', models.PositiveSmallIntegerField(verbose_name='Количество баннеров')),
                ('stopping_sales', models.BooleanField(default=False, verbose_name='Остановка продаж')),
            ],
            options={
                'verbose_name': 'Настройка сайта',
                'verbose_name_plural': 'Настройки сайта',
            },
        ),
    ]
