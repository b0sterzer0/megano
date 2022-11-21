import json
import os

from dotenv import dotenv_values

from market.settings import BASE_DIR


def get_settings():
    path_to_env = os.path.join(BASE_DIR, '../', '.env')
    config = dotenv_values(path_to_env)

    with open(config['PATH_SETTINGS_CONFIG']) as f:
        settings_config = json.load(f)
        return settings_config
