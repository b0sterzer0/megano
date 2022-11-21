from django.db import migrations

from app_settings.utils import get_settings


def create_settings_data(apps, schema_editor):
    settings_config = get_settings()

    SiteSettings = apps.get_model('app_settings', 'SiteSettings')
    SiteSettings.objects.get_or_create(site_name=settings_config['site_name'],
                                       phone_number1=settings_config['phone_number1'],
                                       phone_number2=settings_config['phone_number2'],
                                       address=settings_config['address'],
                                       banner_number=settings_config['banner_number'],
                                       stopping_sales=settings_config['stopping_sales'],
                                       banner_cache_time=settings_config['banner_cache_time'],
                                       total_cache_time=settings_config['total_cache_time']
                                       )


class Migration(migrations.Migration):
    dependencies = [
        ('app_settings', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_settings_data),
    ]
