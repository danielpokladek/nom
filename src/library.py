import os

from pathlib import Path

from aioshutil import copy2
from aioshutil import move

from src.data import current_config
from src.data import DebugLevel
from src.data import FileRenameRecord

map_types = [
    "diffuse", "albedo", "base_color", "base", 
    "specular", "emissive", "emission", "normal",
    "metallic", "roughness", "smoothness", "gloss",
    "ambient", "height", "parallax", "depth",
    "displacement", "opacity", "mask", "detail",
    "flow", "anisotropy", "lightmap", "reflection",
    "lookup", "lut"
]

def retrieveFilesForRenaming(path: Path) -> list[FileRenameRecord]:
    """
    Returns a list of files in the whose names differ 
    from their parsed names, indicating they need to be renamed.
    """
    filesToRename: list[FileRenameRecord] = []
    rawFiles = [file for file in os.listdir(path) if os.path.isfile(Path.joinpath(path, file))]

    for file in rawFiles:
        newFileName = formatFileName(file)
        
        if (file != newFileName):
            filesToRename.append(FileRenameRecord(file, newFileName))

    return filesToRename

def formatFileName(originalFileName: str) -> str:
    """
    Formats a file name by normalizing case, removing zeros, padding numeric
    sequences, replacing separators, and reordering specific keywords based
    on configuration settings. Returns the cleaned file name with its
    original extension.
    """
    split = os.path.splitext(originalFileName)
    file_name = split[0]
    extension = split[1]

    file_name = file_name.lower()

    split_char = current_config.split_char

    processed_parts: list[str] = []
    current_number = ""


    for char in file_name:
        mapped_char = substituteSeparator(char)

        if mapped_char.isnumeric():
            current_number += mapped_char
        else:
            if current_number:
                processed_parts.append(
                    processNumber(current_number)
                )
                current_number = ""

            if mapped_char == current_config.split_char:
                processed_parts.append(split_char)
            else:
                processed_parts.append(mapped_char)

    # Flush any pending number at the end.
    if current_number:
        processed_parts.append(processNumber(current_number))

    clean_file_name = "".join(processed_parts)
    split_words = clean_file_name.split(current_config.split_char)

    # Filter out all empty strings.
    split_words = [word for word in split_words if word]

    has_number_at_end = False

    if split_words and split_words[-1].isnumeric():
        has_number_at_end = True

    if current_config.reorder_map_types == True:
        reorderMapTypes(split_words, has_number_at_end)

    clean_file_name = split_char.join(split_words)

    if current_config.debug_level == DebugLevel.VERBOSE:
        print("Original Name:", originalFileName)
        print("Clean Name:", clean_file_name + extension)
        print("--- --- ---")
        print()

    return clean_file_name + extension

def processNumber(number: str) -> str:
    """
    Cleans a numeric string by removing leading zeros, and applying frame padding.
    """
    try:
        val = int(number)
    except ValueError:
        return number
    
    if current_config.enable_frame_padding:
        return str(val).zfill(current_config.frame_padding)
    
    return str(val)

def substituteSeparator(letter: str):
    """
    Replaces commonly used separators in the input letter with the current
    configuration's `split_char`; returns the original character otherwise.
    """
    split_char = current_config.split_char

    if letter == "-":
        return split_char

    if letter == " ":
        return split_char

    if letter == ".":
        return split_char

    return letter

def handleNumberPadding(characters: list[str], length: int, start_index: int, original_number: str):
    """
    Replaces a sequence of characters with a zero-padded version of original_number, 
    starting at `start_index` and spanning `length` elements.
    Uses the padding from configuration file.
    """
    # Remove the characters associated with the number from array.
    del characters[start_index:start_index + length]
    
    padded_number = original_number.zfill(current_config.frame_padding)

    # Add back the padded number in place of the previous characters.
    characters.insert(
        start_index,
        padded_number
    )

def reorderMapTypes(words_list: list[str], has_number_at_end: bool):
    """
    Reorders elements in `words_list` based on their presence in `map_types`.
    Moves found elements to the end or just before the last item, depending
    on whether there is a number at the end. Modifies `words_list` in place.
    """
    for mapType in map_types:
        if mapType in words_list:
            index = words_list.index(mapType)
            elem = words_list.pop(index)

            if has_number_at_end:
                words_list.insert(len(words_list) - 1, elem)
            else:
                words_list.append(elem)

async def backupAndRenameFiles(path: Path, files_to_rename: list[FileRenameRecord]):
    """
    Backs up each file in files_to_rename from path to a backup
    subdirectory, then renames the original file by copying the backup to
    the new name, preserving metadata. Operates asynchronously.
    """
    backup_path = os.path.join(path, "backup")

    if not os.path.exists(backup_path):
        os.makedirs(backup_path)

    for file in files_to_rename:
        old_name = file.oldName
        new_name = file.newName

        source_file_path = os.path.join(path, old_name)
        backup_file_path = os.path.join(backup_path, old_name)
        newFilePath = os.path.join(path, new_name)

        # Because `copy2` attempts to preserve metadata, it isn't guaranteed
        #  that all of it will be copied successfully - for that reason backup
        #  the original file first, preserving all metadata, and then copy it
        #  to the new location with the new name.
        await move(source_file_path, backup_file_path)
        await copy2(backup_file_path, newFilePath)