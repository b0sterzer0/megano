# Generated by Django 3.2.12 on 2023-03-14 21:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_settings', '0002_data_migration'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sitesettings',
            options={'verbose_name': 'настройка сайта', 'verbose_name_plural': 'настройки сайта'},
        ),
    ]
