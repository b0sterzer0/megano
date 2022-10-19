import json
import os

from django.db import migrations
from dotenv import dotenv_values

from market.settings import BASE_DIR

path_to_env = os.path.join(BASE_DIR, '../', '.env')
config = dotenv_values(path_to_env)


def create_settings_data(apps, schema_editor):
    with open(config['PATH_SETTINGS_CONFIG']) as f:
        settings_config = json.load(f)

    SiteSettings = apps.get_model('app_settings', 'SiteSettings')
    SiteSettings.objects.get_or_create(site_name=settings_config['site_name'],
                                       phone_number1=settings_config['phone_number1'],
                                       phone_number2=settings_config['phone_number2'],
                                       address=settings_config['address'],
                                       banner_number=settings_config['banner_number'],
                                       stopping_sales=settings_config['stopping_sales'],
                                       )


class Migration(migrations.Migration):
    dependencies = [
        ('app_settings', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_settings_data),
    ]
