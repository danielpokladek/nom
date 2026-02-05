import os
import asyncio
import webbrowser

from aioshutil import copy2
from aioshutil import move

from tabulate import tabulate

from src.data import FileRenameRecord

from src.parser import buildParser

from src.config import loadConfig
from src.config import createNewConfig

from src.library import retrieveFilesForRenaming

async def main():
    """
    Main workflow for nom.
    """
    parser = buildParser()
    args = parser.parse_args()
    
    if args.reset:
        promptConfigReset()
        return
    
    if args.config:
        webbrowser.open("nom.config")
        return
    
    loadConfig()
    
    files_path = args.path
    files_to_rename: list[FileRenameRecord] = retrieveFilesForRenaming(files_path)

    if len(files_to_rename) == 0:
        print("No files require renaming.")
        return
    
    printRenamingOverview(files_to_rename)

    if args.dry:
        print()
        print("This was a dry run - no files were actually renamed.")
        return
    
    await backupAndRenameFiles(files_path, files_to_rename)

def promptConfigReset():
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

def printRenamingOverview(files_to_rename: list[FileRenameRecord]):
    """
    Displays an overview of files to be renamed by printing a formatted
    table  - uses tabulate for table formatting.
    """
    tableData: list[list[str]] = []

    for file in files_to_rename:
        tableData.append([file.oldName, file.newName])

    print("Following files will be renamed..")
    print()
    print(tabulate(tableData, headers=["Old Name", "New Name"], tablefmt="rounded_grid"))
    print("Total Files:", len(files_to_rename))

async def backupAndRenameFiles(path: str, files_to_rename: list[FileRenameRecord]):
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

if __name__ == "__main__":
    asyncio.run(main())