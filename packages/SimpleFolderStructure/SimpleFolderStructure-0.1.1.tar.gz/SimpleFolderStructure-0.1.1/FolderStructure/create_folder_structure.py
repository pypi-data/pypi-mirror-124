"""Create directory from formatted file
    Give @ to change directories, can be relative
    NOTE: Look into pathlib rather than os calls
    TODO: Create method to create a file of for a directory
    NOTE: Base64 files more than likely go by direct input or regex
"""
import base64
import logging
import os
# import re
import sys

from colorama import Fore

#pylint: disable=global-statement
PATH = "" #Will be used in creating a directory structure
LOGGER = logging.getLogger()

def _line_change(index: int, line: str):
    """Checks if the path change is valid, if it is changes the path.
        Takes in index for error checking
    """
    global PATH
    line = line[1:]
    if not os.path.isdir(line):
        print(f"ERROR LINE {index}: Folder {line} does not exist.")
        sys.exit(1)
    PATH = os.path.realpath(line) + os.sep
    os.chdir(line)



def _check_names(name: str):
    """Makes sure a folder of file can be created."""
    disallowed = "<>:\"/\\|?*"
    return all(char not in name for char in disallowed)

def _create_files_and_folders(create_type: str, cleaned: str, created: int, errors: int, debug: bool, force: bool):
    """Creates the folder or file base on type."""
    #NOTE: If the amount of types increases, split these into private methods
    #NOTE: If private methods, make a dictionary that holds the methods to not repeat try and expection
    global PATH
    assert PATH[-len(os.sep):] == os.sep, "GLOBAL variable PATH does not end with os seperator"
    cleaned2 = cleaned
    cleaned = PATH + cleaned
    if create_type == "BASE64":
        cleaned2 = cleaned2.split("|")[0]
        base_64_lst = cleaned.split("|")
        cleaned = base_64_lst[0]
        base_64_str = "".join(base_64_lst[1:])
        if not os.path.exists(cleaned) or force:
            if not debug:
                with open(cleaned, "w+", encoding="utf-8") as new_file:
                    new_file.write(base64.b64decode(base_64_str).decode("utf-8"))
            created += 1
        else:
            errors += 1

    elif create_type == "FILE":
        if not os.path.exists(cleaned):
            if not debug:
                with open(cleaned, "w+", encoding="utf-8"):
                    pass
            created += 1
            #Check on first pass

        else:
            errors += 1

    elif create_type == "FOLDER":
        try:
            if not debug:
                os.makedirs(cleaned)
            created += 1
        except FileExistsError:
            errors += 1

    LOGGER.info(PATH + Fore.RED + cleaned2)
    return created, errors


def lint_folder_file(filename: str, prefixs: dict[str,str], indent_char: str = " ", indent_length: int = 4, debug: bool = False, force: bool = False): # sourcery no-metrics
    """Create folders from a file formatted passed in indent charaction and length


    Args:
        filename (str): [description]
        indent_char (str, optional): [description]. Defaults to " ".
        indent_length (int, optional): [description]. Defaults to 4.

    Raises:
        IndentationError: [description]
    """
    global PATH
    PATH = os.path.realpath(os.getcwd()) + os.sep
    with open(filename, "r", encoding="utf-8") as direct_struct:
        recursion_path: list[str] = []
        file_creation = [] #Holds the creation, so we can error check then creates it all after
        errors = 0
        created = 0
        last_indent = 0
        for index, line in enumerate(direct_struct.readlines(), 1):
            indent = -1
            line = line.rstrip().split("//")[0] #Comment splitting
            if len(line) == 0:
                continue
            if line[0] == "@": #Changes directory and resets progress
                _line_change(index, line)
                recursion_path.clear()
                continue
            for key, value in prefixs.items():
                indent = line.find(value)
                if indent != -1:
                    if line[:indent].count(indent_char) != indent:
                        print(f"ERROR LINE {index}: Line {index} contains non-indent character before prefix.")
                        sys.exit(1)
                    create_type = key
                    prefix = value
                    break

            if indent == -1:
                continue
            try:
                cleaned = line.rstrip()[indent:].replace(prefix, "")
                if indent == 0:
                    recursion_path.clear()
                    recursion_path.append(cleaned)

                elif indent < last_indent:
                    while len(recursion_path) != indent//indent_length:
                        recursion_path.pop()
                    recursion_path.append(cleaned)

                elif indent == indent_length:
                    if len(recursion_path) == 1:
                        recursion_path.append(cleaned)
                    else:
                        recursion_path[1] = cleaned

                elif indent == len(recursion_path) *indent_length:
                    recursion_path.append(cleaned)
                else:
                    recursion_path[indent//indent_length] = cleaned
                if indent % indent_length != 0:
                    raise IndentationError()
                last_indent = indent
            except IndexError: #Over indenting
                print(f"ERROR LINE {index}: Line {index} must be indented in order")
                print(f"Current indent length: {indent}")
                path_length = len(recursion_path)
                print(f"Possible lengths: {'0' if path_length == 0 else str(path_length*indent_length) + ' or any multiple of ' + str(indent_length) + ' below it.'}")
                sys.exit(1)
            except IndentationError: #Bad under indenting
                print(f"ERROR LINE {index}: Line {index} must be indented in properly")
                print(f"Current indent length: {indent}")
                path_length = len(recursion_path)
                print(f"Must be a multiple of {indent_length}")
                print(f"Closest indents: {indent - indent%indent_length}, {indent - indent%indent_length+indent_length}")
                sys.exit(1)

            if create_type != "BASE64" and not _check_names(cleaned):
                print(f"ERROR LINE {index}: couldn't create {create_type} from Line {index}. Are there dissallowed characters in the name?")
                sys.exit(1)
            file_creation.append((create_type, os.sep.join(recursion_path))) # Split for text color

        assert len(prefixs) == 3, "You've added a new file type, please add another method"
        for (file_type, file_path) in file_creation:
            created, errors = _create_files_and_folders(create_type=file_type, cleaned=file_path, created=created, errors=errors, debug=debug, force=force)


        print(f"Created {created} file{'' if created == 1 else 's'}, {errors} file{'' if errors == 1 else 's'} already existed.")
