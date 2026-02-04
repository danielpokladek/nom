import os

from configparser import ConfigParser
from dataclasses import dataclass

@dataclass
class Config:
    split_char: str = ""
    frame_padding: int = 0
    debug_level: int = 1

config_name = "nom.config"

current_config = Config()

def loadConfig():
    if not os.path.isfile(config_name):
        createNewConfig()

    config = ConfigParser()
    config.read(config_name)

    file_settings = config["FILE_SETTINGS"]
    current_config.split_char = file_settings["split_char"]
    current_config.frame_padding = int(file_settings["frame_padding"])

    app_settings = config["APP_SETTINGS"]
    current_config.debug_level = int(app_settings["debug_level"])

def createNewConfig():
    config = ConfigParser()
    config["FILE_SETTINGS"] = {
        "split_char": "_",
        "frame_padding": "3",
        "debug_level": "1"
    }

    with open(config_name, mode="w", encoding="utf-8") as config_file:
        config.write(config_file)