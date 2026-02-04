import os
import asyncio
import argparse
import webbrowser

from dataclasses import dataclass

from aioshutil import copy2
from enum import Enum
from tabulate import tabulate

from src.config import loadConfig
from src.config import createNewConfig
from src.config import current_config

class Debug(Enum):
    NORMAL = 1
    VERBOSE = 2

map_types = ["diffuse", "albedo", "normal", "roughness"]

async def main():
    args = setupParser()

    if args.reset:
        handleConfigReset()
        return

    loadConfig()

    if args.config:
        webbrowser.open("nom.config")
        return

    files_to_rename: list[OldNewFileClass] = getFilesToRename()

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

def setupParser():
    parser = argparse.ArgumentParser(
        prog="nom",
        description="Normalize Our Mess - CLI tool for rule-based asset renaming.",
        add_help=False
    )

    required = parser.add_argument_group("required arguments")
    required.add_argument(
        "-p", "--path",
        help="Path to directory where assets should be organized."
    )

    optional = parser.add_argument_group("optional arguments")
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

    return parser.parse_args()

def handleConfigReset():
    user_input = input("Are you sure you want to reset the config to default state? [y/N]: ")

    if user_input.lower() == "y" or user_input.lower() == "yes":
        createNewConfig()

        print("Config has been reset to default state!")
        return
    else:
        return

@dataclass
class OldNewFileClass:
    oldName: str
    newName: str

def getFilesToRename() -> list[OldNewFileClass]:
    filesToRename: list[OldNewFileClass] = []
    rawFiles = [file for file in os.listdir('./test') if os.path.isfile("./test/" + file)]

    for file in rawFiles:
        newFileName = parseFileName(file)
        
        if (file != newFileName):
            filesToRename.append(OldNewFileClass(file, newFileName))

    return filesToRename

def parseFileName(originalFileName: str) -> str:
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

        letters[i] = parseSeparator(letters[i])
    
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

def parseSeparator(letter: str):
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