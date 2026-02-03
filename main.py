import os
from enum import Enum

class Debug(Enum):
    NORMAL = 1
    VERBOSE = 2

DEBUG_LEVEL = Debug.VERBOSE

splitChar = "_"
fileList = []

def main():
    for subdir, dirs, files in os.walk("./test"):
        for file in files:
            parseFileName(file)

    # parseFileName("frame METAL_albedo_test-NoRmAL 012.png")
            

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

        if letters[i] == splitChar:
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
    cleanFileName = cleanFileName + extension

    print("Original Name:", originalFileName)

    if DEBUG_LEVEL == Debug.VERBOSE:
        print(letters)

    print("Clean Name:", cleanFileName)
    print("--- --- ---")
    print()

def parseSeparator(letter, separator):
    if letter == "-":
        return splitChar

    if letter == " ":
        return splitChar

    if letter == ".":
        return splitChar

    return letter

if __name__ == "__main__":
    main()