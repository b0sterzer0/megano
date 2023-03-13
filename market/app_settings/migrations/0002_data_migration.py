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
                                       total_cache_time=settings_config['total_cache_time'],
                                       seller_cache_time=settings_config['seller_cache_time'],
                                       sellers_products_top_cache_time=settings_config[
                                           'sellers_products_top_cache_time'],
                                       sellers_products_top_number=settings_config['sellers_products_top_number'],
                                       common_products_top_number=settings_config['common_products_top_number'],
                                       ordinary_delivery_cost=settings_config['ordinary_delivery_cost'],
                                       min_amount_for_free_delivery=settings_config['min_amount_for_free_delivery'],
                                       express_delivery_cost=settings_config['express_delivery_cost']

                                       )


class Migration(migrations.Migration):
    dependencies = [
        ('app_settings', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_settings_data),
    ]
