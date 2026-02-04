import os

from configparser import ConfigParser

config_name = "nom.config"

current_config = {
    "split_char": "",
    "frame_padding": 0,
    "debug_level": 1
}

def loadConfig():
    if not os.path.isfile(config_name):
        createNewConfig()

    config = ConfigParser()
    config.read(config_name)

    file_settings = config["FILE_SETTINGS"]
    current_config["split_char"] = file_settings["split_char"]
    current_config["frame_padding"] = file_settings["frame_padding"]

    app_settings = config["APP_SETTINGS"]
    current_config["debug_level"] = app_settings["debug_level"]

def createNewConfig():
    config = ConfigParser()
    config["FILE_SETTINGS"] = {
        "split_char": "_",
        "frame_padding": 3
    }

    with open(config_name, mode="w", encoding="utf-8") as config_file:
        config.write(config_file)