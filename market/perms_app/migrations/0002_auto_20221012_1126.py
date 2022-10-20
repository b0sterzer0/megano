# Generated by Django 3.2.12 on 2022-10-12 08:26
from django.contrib.auth.management import create_permissions
from django.db import migrations
import json
from pathlib import Path


def load_roles(apps, schema_editor):
    """
    Создание ролей и распределение разрешений
    """

    # Явно запускаем процесс создания Разрешений у моделей Django.
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, verbosity=0)
        app_config.models_module = None

    # Импортируем модели
    Group = apps.get_model("auth.Group")
    Permission = apps.get_model("auth.Permission")

    # Загружаем роли и разрешения из json файла
    path = Path(Path.cwd(), 'perms_app', 'fixtures', 'auth_groups.json')
    with open(path) as file:
        data = json.load(file)
        for elem in data:
            group = Group.objects.create(name=elem['fields']['name'])
            # Выбираем все существующие роли для группы пользователей.
            permissions = Permission.objects.filter(id__in=elem['fields']['permissions'])
            # Добавляем их к группе
            group.permissions.set(permissions)
            group.save()


class Migration(migrations.Migration):

    dependencies = [
        ('perms_app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_roles),
    ]