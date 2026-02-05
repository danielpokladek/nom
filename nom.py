import asyncio
import webbrowser
import sys
import time

from tabulate import tabulate
from pathlib import Path

from src.data import FileRenameRecord
from src.data import ascii_logo
from src.data import current_config

from src.parser import buildParser

from src.config import loadConfig
from src.config import createNewConfig

from src.library import retrieveFilesForRenaming
from src.library import backupAndRenameFiles

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
        tableData.append([file.old_name, file.new_name])

    print("Following files will be renamed..")
    print()
    print(tabulate(tableData, headers=["Old Name", "New Name"], tablefmt="rounded_grid"))
    print("Total Files:", len(files_to_rename))

def playAnimation(files_number: int = 3):
    """
    Plays an animation of eating the files represented as dots from left to right.
    """
    mouth_open = "<" 
    mouth_closed = "-"

    target_text = ""

    for _ in range(files_number):
        target_text += "."

    # Ensure cursor is at start
    sys.stdout.write("\r")
    
    for i in range(files_number + 1):
        character = mouth_open if i % 2 == 0 else mouth_closed
        
        frame = " " * i + character + target_text[i:]
        
        # Write to stdout without a newline, then flush buffer
        sys.stdout.write(f"\r{frame}")
        sys.stdout.flush()
        
        # Speed of animation
        time.sleep(0.15)

    # Clean up the line when done
    sys.stdout.write(f"\r{' ' * (files_number + 1)}\r")
    sys.stdout.flush()

async def main():
    """
    Main workflow for nom.
    """
    parser = buildParser()
    
    # If no params have been passed, print help.
    if not len(sys.argv) > 1:
        parser.print_help()
        return
        
    args = parser.parse_args()
    
    if args.reset:
        promptConfigReset()
        return
    
    if args.config:
        webbrowser.open("nom.config")
        return
    
    loadConfig()

    if not args.no_logo and current_config.show_logo:
        print(ascii_logo)
    
    files_path = Path(args.path).resolve()

    if not files_path.exists():
        print("Invalid Path : Directory does not exist!")
        return

    files_to_rename: list[FileRenameRecord] = retrieveFilesForRenaming(files_path)

    if len(files_to_rename) == 0:
        print("No files require renaming.")
        return
    
    printRenamingOverview(files_to_rename)
    playAnimation(len(files_to_rename))

    if args.dry:
        print()
        print("This was a dry run - no files were actually renamed.")
        return
    
    await backupAndRenameFiles(files_path, files_to_rename)

if __name__ == "__main__":
    asyncio.run(main())