import argparse

_parser: argparse.ArgumentParser

def buildParser():
    """
    Creates and configures an argparse.ArgumentParser for the "nom" CLI
    tool, defining required and optional command-line arguments for asset
    renaming operations.
    """
    _parser = argparse.ArgumentParser(
        prog="nom",
        description="Normalize Our Mess - CLI tool for rule-based asset renaming.",
        add_help=False
    )

    required = _parser.add_argument_group("required arguments")
    required.add_argument(
        "-p", "--path",
        help="Path to directory where assets should be organized."
    )

    optional = _parser.add_argument_group("optional arguments")
    optional.add_argument(
        "-r", "--reset", action="store_true",
        help="Resets config to original state."
    )
    optional.add_argument(
        "-d", "--dry", action="store_true",
        help="Dry run - shows what files would be renamed without actually renaming them."
    )
    optional.add_argument(
        "-c", "--config", action="store_true",
        help="Open config file in system default text editor."
    )
    optional.add_argument(
        "-h", "--help", action="help",
        help="Show this help message and exit."
    )

def getParserArgs():
    """
    Returns the parsed command-line arguments as a Namespace object using
    _parser.parse_args().
    """
    return _parser.parse_args()