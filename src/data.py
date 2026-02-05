from enum import Enum
from dataclasses import dataclass

@dataclass
class Config:
    split_char: str = ""
    frame_padding: int = 0
    debug_level: int = 1

class DebugLevel(Enum):
    """
    Represents debug output levels with two options: NORMAL for standard
    output and VERBOSE for detailed output.
    """
    NORMAL = 1
    VERBOSE = 2

@dataclass
class FileRenameRecord:
    """
    Represents a file renaming record, storing the oldName and newName as strings.
    """
    oldName: str
    newName: str

current_config = Config()