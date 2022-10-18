from django.apps import AppConfig


class AppSettingsConfig(AppConfig):
    """Класс конфигурации приложения настроек сайта"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_settings'
