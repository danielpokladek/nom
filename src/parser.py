import argparse

def buildParser():
    """
    Creates and configures an argparse.ArgumentParser for the "nom" CLI
    tool, defining required and optional command-line arguments for asset
    renaming operations.
    """
    parser = argparse.ArgumentParser(
        prog="nom",
        description="Normalize Our Mess - CLI tool for rule-based asset renaming.",
        add_help=False
    )

    required = parser.add_argument_group("required arguments")
    required.add_argument(
        "-p", "--path",
        help="Path to directory containing files/assets which need renaming."
    )

    optional = parser.add_argument_group("optional arguments")
    optional.add_argument(
        "-d", "--dry", action="store_true",
        help="Dry run - shows what files would be renamed without actually renaming them."
    )

    settings = parser.add_argument_group("settings arguments")
    settings.add_argument(
        "-r", "--reset", action="store_true",
        help="Resets the configuration file to it's default state."
    )
    settings.add_argument(
        "-c", "--config", action="store_true",
        help="Open configuration file using the default text editor."
    )
    settings.add_argument(
        "-h", "--help", action="help",
        help="Show this help message and exit."
    )

    return parser