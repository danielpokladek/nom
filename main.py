import os

splitChar = "_"
fileList = []

def main():
    choice = 0

    # while choice != 4:
    #     print("*** File List ***")
    #     print("1) Option A")
    #     print("2) Option B")
    #     print("3) Option C")
    #     print("4) Quit")
    #     choice = int(input())

    # for subdir, dirs, files in os.walk("./test"):
    #     for file in files:
    #         parseFileName(file)

    parseFileName("frame METAL_albedo_test-NoRmAL.png")
            

def parseFileName(originalFileName):
    split = os.path.splitext(originalFileName)
    fileName = split[0]
    extension = split[1]
    # words = splitPath.split()
    
    cleanFileName = ""

    # for i in shortFileName:
    letters = list(fileName)
    
    for i in range(len(letters)):
        letters[i] = letters[i].lower()

        if letters[i] == splitChar:
            continue

        if letters[i] == "-":
            letters[i] = splitChar

        if letters[i] == " ":
            letters[i] = splitChar

        if letters[i] == ".":
            letters[i] = splitChar
            

    print(letters)
    print("".join(letters))
    cleanFileName = "".join(letters)

    print(originalFileName)
    print("Split Name: " + fileName)
    # print("Words In Name:", words)
    print("Clean File Name:", cleanFileName)
    print("Clean With Extension:", cleanFileName + extension)
    print("--- --- ---")
    print()

def removeSeparator(text, separator):
    splitWords = text.split(separator)

    return splitWords

if __name__ == "__main__":
    main()