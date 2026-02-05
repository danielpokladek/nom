from enum import Enum
from dataclasses import dataclass

@dataclass
class Config:
    """
    Represents configuration settings with fields. Uses Python's 
    dataclass for automatic method generation.
    """
    show_logo: bool = True
    split_char: str = ""
    enable_frame_padding: bool = True
    frame_padding: int = 0
    reorder_map_types: bool = True
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
    old_name: str
    new_name: str

ascii_logo = r"""
          _____                   _______                   _____          
         /\    \                 /::\    \                 /\    \         
        /::\____\               /::::\    \               /::\____\        
       /::::|   |              /::::::\    \             /::::|   |        
      /:::::|   |             /::::::::\    \           /:::::|   |        
     /::::::|   |            /:::/~~\:::\    \         /::::::|   |        
    /:::/|::|   |           /:::/    \:::\    \       /:::/|::|   |        
   /:::/ |::|   |          /:::/    / \:::\    \     /:::/ |::|   |        
  /:::/  |::|   | _____   /:::/____/   \:::\____\   /:::/  |::|___|______  
 /:::/   |::|   |/\    \ |:::|    |     |:::|    | /:::/   |::::::::\    \ 
/:: /    |::|   /::\____\|:::|____|     |:::|    |/:::/    |:::::::::\____\
\::/    /|::|  /:::/    / \:::\    \   /:::/    / \::/    / ~~~~~/:::/    /
 \/____/ |::| /:::/    /   \:::\    \ /:::/    /   \/____/      /:::/    / 
         |::|/:::/    /     \:::\    /:::/    /                /:::/    /  
         |::::::/    /       \:::\__/:::/    /                /:::/    /   
         |:::::/    /         \::::::::/    /                /:::/    /    
         |::::/    /           \::::::/    /                /:::/    /     
         /:::/    /             \::::/    /                /:::/    /      
        /:::/    /               \::/____/                /:::/    /       
        \::/    /                 ~~                      \::/    /        
         \/____/                                           \/____/  

You make the mess, we normalize it..
"""

current_config = Config()