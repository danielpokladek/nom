import os
import asyncio
import webbrowser

from dataclasses import dataclass

from aioshutil import copy2
from enum import Enum
from tabulate import tabulate

from src.parser import buildParser
from src.parser import getParserArgs

from src.config import loadConfig
from src.config import createNewConfig
from src.config import current_config

class Debug(Enum):
    """
    Represents debug output levels with two options: NORMAL for standard
    output and VERBOSE for detailed output.
    """
    NORMAL = 1
    VERBOSE = 2

map_types = ["diffuse", "albedo", "normal", "roughness"]

async def main():
    """
    Main workflow for nom.
    """
    buildParser()
    args = getParserArgs()
    
    if args.reset:
        handleConfigReset()
        return
    
    if args.config:
        webbrowser.open("nom.config")
        return
    
    loadConfig()

    files_to_rename: list[OldNewFileClass] = listFilesNeedingRename()

    if len(files_to_rename) == 0:
        print("No files to rename - have a good day!")
        return
    
    tableData: list[list[str]] = []

    for file in files_to_rename:
        tableData.append([file.oldName, file.newName])

    print("Following files will be renamed..")
    print()
    print(tabulate(tableData, headers=["Old Name", "New Name"]))

    if not os.path.exists("./test/original"):
        os.makedirs("./test/original")

    if args.dry:
        print()
        print("This was a dry run - no files were actually renamed.")
        return

    for file in files_to_rename:
        old_name = file.oldName
        new_name = file.newName

        await copy2(f'./test/{old_name}', f'./test/original/{old_name}')

        os.rename("./test/" + old_name, "./test/" + new_name)

def handleConfigReset():
    """
    Prompts the user for confirmation and, if confirmed, resets the
    configuration to its default state.
    """
    user_input = input("Are you sure you want to reset the config to default state? [y/N]: ")

    if user_input.lower() == "y" or user_input.lower() == "yes":
        createNewConfig()

        print("Config has been reset to default state!")
        return
    else:
        return

@dataclass
class OldNewFileClass:
    """
    Represents a file renaming operation, storing the oldName and newName as
    strings.
    """
    oldName: str
    newName: str

def listFilesNeedingRename() -> list[OldNewFileClass]:
    """
    Returns a list of files in the whose names differ 
    from their parsed names, indicating they need to be renamed.
    """
    filesToRename: list[OldNewFileClass] = []
    rawFiles = [file for file in os.listdir('./test') if os.path.isfile("./test/" + file)]

    for file in rawFiles:
        newFileName = formatFileName(file)
        
        if (file != newFileName):
            filesToRename.append(OldNewFileClass(file, newFileName))

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

    if current_config.debug_level == Debug.VERBOSE:
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

if __name__ == "__main__":
    asyncio.run(main())