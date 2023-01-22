import json
import os

from dotenv import dotenv_values

from market.settings import BASE_DIR


def get_settings():
    """Функция загружает настройки для сайта."""
    path_to_env = os.path.join(BASE_DIR, '../', '.env')
    config = dotenv_values(path_to_env)

    with open(config['PATH_SETTINGS_CONFIG'], encoding='utf-8') as file:
        settings_config = json.load(file)
        return settings_config
