import os

from platformdirs import user_config_path
from configparser import ConfigParser

from src.data import DebugLevel
from src.data import current_config

app_name = "nom"
app_author = "dpokladek"

config_name = "nom.config"
path_to_config = user_config_path(app_name, app_author)
full_path = os.path.join(path_to_config, config_name)

def loadConfig():
    """
    Loads configuration settings from a file, creating a new config if
    missing, and updates current_config with values from the relevant
    config sections.
    """

    if not os.path.isfile(full_path):
        createNewConfig()

    config = ConfigParser()
    config.read(full_path)

    file_settings = config["FILE_SETTINGS"]
    current_config.show_logo = bool(file_settings["show_logo"])
    current_config.split_char = file_settings["split_char"]
    current_config.frame_padding = int(file_settings["frame_padding"])
    current_config.enable_frame_padding = bool(file_settings["enable_frame_padding"])
    current_config.reorder_map_types = bool(file_settings["reorder_map_types"])

    app_settings = config["APP_SETTINGS"]
    current_config.debug_level = int(app_settings["debug_level"])

def createNewConfig():
    """
    Creates a new configuration file with default settings using ConfigParser.
    """
    config = ConfigParser()
    config["FILE_SETTINGS"] = {
        "show_logo": "True",
        "split_char": "_",
        "frame_padding": "3",
        "enable_frame_padding": "True",
        "reorder_map_types": "True",
    }

    config["APP_SETTINGS"] = {
        "debug_level": "1"
    }

    if current_config.debug_level == DebugLevel.VERBOSE:
        print("Creating new config file with default properties..")
        print("If config already exists, it will be overwritten")

    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    with open(full_path, mode="w", encoding="utf-8") as config_file:
        config.write(config_file)