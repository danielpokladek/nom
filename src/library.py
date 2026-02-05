import os

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

def retrieveFilesForRenaming(path: str) -> list[FileRenameRecord]:
    """
    Returns a list of files in the whose names differ 
    from their parsed names, indicating they need to be renamed.
    """
    filesToRename: list[FileRenameRecord] = []
    rawFiles = [file for file in os.listdir(path) if os.path.isfile(path + file)]

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
    fileName = split[0]
    extension = split[1]
    
    cleanFileName = ""
    letters = list(fileName)

    wasPreviousNumber = False
    numberStartIndex = 0
    numberLength = 1
    number = ""

    split_char = current_config.split_char
    frame_padding = current_config.frame_padding
    
    for i in range(len(letters)):
        letters[i] = letters[i].lower()

        if letters[i] == split_char:
            continue

        if letters[i] == "0":
            letters[i] = ""
            continue

        if letters[i].isnumeric():
            if wasPreviousNumber:
                number += letters[i]
                numberLength += 1
            else:
                number = letters[i]
                numberStartIndex = i
                numberLength = 1
                wasPreviousNumber = True
        else:
            wasPreviousNumber = False

        letters[i] = substituteSeparator(letters[i])
    
    if number != "":
        for i in range(numberLength):
            letters.pop(numberStartIndex)

        letters.insert(numberStartIndex, number.zfill(frame_padding))

    cleanFileName = "".join(letters)

    splitWords = cleanFileName.split("_")

    if "" in splitWords:
        splitWords.remove("")

    for mapType in map_types:
        if mapType in splitWords:
            index = splitWords.index(mapType)
            elem = splitWords.pop(index)

            if number == "":
                splitWords.append(elem)
            else:
                splitWords.insert(len(splitWords) - 1, elem)

    cleanFileName = "_".join(splitWords)

    if current_config.debug_level == DebugLevel.VERBOSE:
        print("Original Name:", originalFileName)
        print(letters)

        print("Clean Name:", cleanFileName + extension)
        print("--- --- ---")
        print()

    return cleanFileName + extension

def substituteSeparator(letter: str):
    """
    Replaces commonly used separators in the input letter with the current
    configuration's split_char; returns the original character otherwise.
    """
    split_char = current_config.split_char

    if letter == "-":
        return split_char

    if letter == " ":
        return split_char

    if letter == ".":
        return split_char

    return letter