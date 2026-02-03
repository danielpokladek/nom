import os
import asyncio

from aioshutil import copy2
from enum import Enum
from tabulate import tabulate

class Debug(Enum):
    NORMAL = 1
    VERBOSE = 2

debug_level = Debug.NORMAL
map_types = ["diffuse", "albedo", "normal", "roughness"]
split_char = "_"

async def main():
    filesToRename = getFilesToRename()

    if len(filesToRename) == 0:
        print("No files to rename - have a good day!")
        return

    print("Following files will be renamed..")
    print()
    print(tabulate(filesToRename, headers=["Old Name", "New Name"]))

    if not os.path.exists("./test/original"):
        os.makedirs("./test/original")

    for file in filesToRename:
        oldName = file[0]
        newName = file[1]

        await copy2(f'./test/{oldName}', f'./test/original/{oldName}')

        os.rename("./test/" + oldName, "./test/" + newName)

def getFilesToRename():
    filesToRename = []
    rawFiles = [file for file in os.listdir('./test') if os.path.isfile("./test/" + file)]

    for file in rawFiles:
        newFileName = parseFileName(file)
        
        if (file != newFileName):
            filesToRename.append([file, newFileName])

    return filesToRename

def parseFileName(originalFileName):
    split = os.path.splitext(originalFileName)
    fileName = split[0]
    extension = split[1]
    
    cleanFileName = ""
    letters = list(fileName)

    wasPreviousNumber = False
    numberStartIndex = 0
    numberLength = 1
    number = ""
    
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

        letters[i] = parseSeparator(letters[i], "-")
        letters[i] = parseSeparator(letters[i], ".")
        letters[i] = parseSeparator(letters[i], " ")
    
    if number != "":
        for i in range(numberLength):
            letters.pop(numberStartIndex)

        letters.insert(numberStartIndex, number.zfill(3))

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

    if debug_level == Debug.VERBOSE:
        print("Original Name:", originalFileName)
        print(letters)

        print("Clean Name:", cleanFileName + extension)
        print("--- --- ---")
        print()

    return cleanFileName + extension

def parseSeparator(letter, separator):
    if letter == "-":
        return split_char

    if letter == " ":
        return split_char

    if letter == ".":
        return split_char

    return letter

if __name__ == "__main__":
    asyncio.run(main())