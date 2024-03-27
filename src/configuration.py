import configparser
import os
from dataclasses import dataclass


@dataclass
class AppConfig:
    admin_token: str


def configuration() -> AppConfig:
    path = os.environ.get("SETTINGS_PATH", "resources/config.ini")
    config = configparser.ConfigParser()
    config.read(path)
    return AppConfig(
        admin_token=config['auth']['admin_token']
    )
