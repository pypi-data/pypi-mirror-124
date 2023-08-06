"""Create directory from formatted file
    Give @ to change directories, can be relative
    NOTE: Look into pathlib rather than os calls
    TODO: New features (In order of implementing):
        Finish the readme
        Steal test structure from porth (https://gitlab.com/tsoding/porth/-/blob/master/test.py)
        Add a configuration file so that command line doesn't have ot be filled with args
        Add input for Folder names. EX: (Name for new folder) -> input("Name for the new folder: ")
        Add files that can take input on creation. Idea is to use it for things like setup.
            Add args for opening and closing character to account for different file types
            Add ability to add variables
    mypy {filename} --ignore-missing-imports #This is for colorama
"""

import logging
import os
import re
import sys
import time
from argparse import ArgumentParser, ArgumentTypeError

from colorama import Fore, Style, init
try:
    from FolderStructure.create_folder_structure import lint_folder_file#doing it here to try and make logger work
    from FolderStructure.generate_folder_structure import FileFilter, lint_generate_file
except ImportError:
    from create_folder_structure import lint_folder_file
    from generate_folder_structure import FileFilter, lint_generate_file


#pylint: disable=global-statement
class CustomFormatter(logging.Formatter):
    "Removes the color from the log before sending it to the log"
    def format(self, record):
        record.msg = record.msg.replace(Fore.RED, '')
        return super().format(record)


#Create the base logger so every other logger will also log to it
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
FORMATTERSH =  logging.Formatter('%(message)s')
FORMATTERFH =  CustomFormatter('%(message)s')
#colorama setup
init(autoreset=True, convert=True, strip=True)


class HelpOutputParser(ArgumentParser):
    """This class exists to overwrite the error class in arg parse, so that help will print on all errors
    """
    def error(self, message):
        if len(sys.argv) != 1: # An argument was passed in
            message = message.split(":")
            front_mess = message[0]
            back_mess = ":".join(message[1:]) if len(message) > 1 else ""
            sys.stderr.write(f'{Fore.RED}ERROR: {front_mess}:{Style.RESET_ALL}{back_mess}\n\n')
            self.print_usage(sys.stderr)
        else:
            self.print_help(sys.stderr)
        sys.exit(2)

def re_compile(pattern: str):
    "Returns a compiled pattern, theres a chance i don't need this since the repr returns a re.compile rather than Pattern('pattern')"
    return re.compile(pattern)


def dir_path(path: str) -> str:
    """Checks if a path is real and returns the full path, else error's out"""
    if os.path.exists(path):
        return os.path.realpath(path, strict=True) #technically with the exists i shouldn't need this but makes it safer probably
    raise ArgumentTypeError(f"Output directory \"{path}\" is not a valid path")


def file_path_verification(path: str, willcreatethefile: bool) -> str:
    """Checks if a path is real and returns the full path, else error's out.
    If createfile is true, will not return an error if file doesn't exist
    If createfile is false, will return an error on missing

    The difference from dir_path is this outputs a input file error message -_-"""
    if os.path.exists(path) or willcreatethefile:
        return os.path.realpath(path)# technically with the exists i shouldn't need this but makes it safer probably
    raise ArgumentTypeError(f"Input file \"{path}\" is not a valid path")


def main():
    """
    Have a regex for which files to use base on
    Also just allow them to specify a filetype(s)
    """
    #NOTE: We could change it from just prefixs to a class that allows us to keep track of exactly whats created and errors
    prefixs = {
    'BASE64': '? ',
    'FILE': ': ' ,
    'FOLDER': '* '
    }


    global LOGGER
    parser = HelpOutputParser(description="Save or Create a directory structure.")
    parser.add_argument('action', type=lambda x: str(x).lower(), choices=['save', 'create'], help='Choose whether to create a directory from a file or save a directory to a file.')
    parser.add_argument("file", type=str, help="The file to read from to create the directory/write to to save the directory.") #Cant do file check due to being read or write
    parser.add_argument('save', action="store_true", help='Creates a directory from a file')

    group = parser.add_argument_group("Logging option")
    group.add_argument('-v', '--verbosity', action="store_true", help='Print out the full path of each item created')
    group.add_argument('-l', '--log', action="store_true", help='Output the full path of each item created to a log')
    group.add_argument('-d', '--debug', action="store_true", help="Don't create any files or folders. Will turn on -v for console output")

    group = parser.add_argument_group('Output of directory/file')
    group.add_argument('-o', '--output', type=dir_path, help='The directory to createthe directory found in the file/to save to file', default=os.path.realpath(os.getcwd()))

    group = parser.add_argument_group("Indent and prefix modification. Default's are all non allowed chars in files and folders")
    group.add_argument("-s", "--size", type=int, help="The size of the indent character(4 spaces in 1 indent, 1 asterisk per indent or 2 ':;' per indent(':;:;'))", default=4)
    group.add_argument("-c", "--character", type=str, help="The character(s) that fill in the indent (' ' a single space or '*' asterisk or ':;' colon semi colon)", default=" ")

    #Add prefix changes to arguments
    group = parser.add_argument_group('Prefix Control')
    for key, value in prefixs.items():
        group.add_argument(f'--{key}PRE', type=str, help=f"The prefix for type {key}. Default \"{value}\"", default=value)

    group = parser.add_argument_group("Saving directory specific switches. EXCLUDES TAKE PRIORITY OVER INCLUDES")
    group.add_argument('-exfold', '--excludefolder', nargs='+', type=re_compile, help='Excludes a folder from being added to the list. Can have multiple regex expression checked against', default=set()) #Finish args
    group.add_argument('-extype', '--excludetype', nargs='+', type=str, help='Excludes a type from being added to the list. Allows for multiple types.', default=set()) #Finish args
    group.add_argument('-exrex', '--excluderegex', nargs='+', type=re_compile, help='Excludes a file from being added to the list by checking with regex. Allows for multple patterns.', default=set()) #Finish args
    group.add_argument('-intype', '--includetype', nargs='+', type=str, help='Types for adding the contents of a file to the list in BASE64. Can have multiple types checked against', default=set()) #Finish args
    group.add_argument('-inrex', '--includeregex', nargs='+', type=re_compile, help='Patterns for adding the contents of a file to the list in BASE64. Can have multiple patterns checked against', default=set()) #Finish args

    group = parser.add_argument_group('Creating directory specific switches')
    group.add_argument('-f', '--force', action="store_true", help='Rewrites all files even if they already exist.')
    try:
        args = parser.parse_args()
    except re.error as re_ex:
        print(f"couldn't parse given argument '{re_ex.pattern}'. Error: '{re_ex.args[0]}'")
        sys.exit(1)



    #Add stdout to log if selected
    if args.verbosity or args.debug: #We have to check verbosity first or else the removal of the color will affect the console output
        slh = logging.StreamHandler(sys.stdout)
        slh.setFormatter(FORMATTERSH)
        LOGGER.addHandler(slh)

    #Add filehandler to lof if selected
    if args.log:
        flh = logging.FileHandler(filename=args.output + os.sep + f"CREATED_FOLDERS_AND_FILES{time.strftime('_H%H_M%M_%d_%m_%Y')}.log", mode='w')
        flh.setFormatter(FORMATTERFH)
        LOGGER.addHandler(flh)

    #get path before the directory may change
    args.file = os.path.realpath(args.file)

    #Fix path, it's only used for coloring the output text
    os.chdir(args.output)
    #update prefixs
    for key in prefixs:
        prefixs[key] = args.__dict__[key+"PRE"]
    if args.action == "save":
        args.file = file_path_verification(args.file, True)
        fil = FileFilter(
            excluded_file_regex=set(args.excluderegex),
            excluded_file_types=set(args.excludetype),
            excluded_folder_regex=set(args.excludefolder),
            included_file_regex=set(args.includeregex),
            included_file_types=set(args.includetype)
        )
        lint_generate_file(filename=os.path.realpath(args.file), prefixs=prefixs, file_parser=fil, indent_real=args.character*args.size, debug=args.debug)
    else:
        args.file = file_path_verification(args.file, False)
        lint_folder_file(filename=os.path.realpath(args.file), prefixs=prefixs, indent_char=args.character, indent_length=args.size, debug=args.debug, force=args.force)

if __name__ == "__main__":
    main()
