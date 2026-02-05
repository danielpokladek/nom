import os

from configparser import ConfigParser

from src.data import DebugLevel
from src.data import current_config

config_name = "nom.config"

def loadConfig():
    """
    Loads configuration settings from a file, creating a new config if
    missing, and updates current_config with values from the relevant
    config sections.
    """
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
    """
    Creates a new configuration file with default settings using ConfigParser.
    """
    config = ConfigParser()
    config["FILE_SETTINGS"] = {
        "split_char": "_",
        "frame_padding": "3",
        "debug_level": "1"
    }

    if current_config.debug_level == DebugLevel.VERBOSE:
        print("Creating new config file with default properties..")
        print("If config already exists, it will be overwritten")

    with open(config_name, mode="w", encoding="utf-8") as config_file:
        config.write(config_file)