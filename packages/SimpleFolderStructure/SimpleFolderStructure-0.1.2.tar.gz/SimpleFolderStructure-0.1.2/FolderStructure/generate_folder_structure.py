"""Creates a file for sharing of a directory structure

    TODO: Change output of files so that folders are done before base files
"""
import base64
import logging
import os
import re
from dataclasses import dataclass, field


#pylint: disable=global-statement
#Will be used in creating a directory structure
LOGGER = logging.getLogger()

@dataclass
class FileFilter():
    """
    Holds the included and excluded file types to parse in the generator
    Included files is specificity for BASE64 files, saving the contents of the folder withing the outputted file
    All folders are included by default since we don't CURRENTLY have a kind of folder similar to BASE64
    ^
    Maybe a zip file folder that instead zips stuff up. But that sounds stupid and not useful for now.

    Excluded file will make it so files aren't added to the output file at all. Used for hiding stuff with personal names or something idk
    Excluded folder will make it so that it won't register anything from the path onwards

    Ex: c://folder1//folder2 is on the excluded folder list
    it will not capture that folder or the next subfolders after ti
    but will capture
    c://folder1//folder3 instead

    """

    # included
    included_file_types: set[str] | None = None
    included_file_regex: set[re.Pattern] | None = None
    # Excluded
    excluded_file_types: set[str] = field(default_factory=set)
    excluded_file_regex: set[re.Pattern] = field(default_factory=set)
    excluded_folder_regex: set[re.Pattern] = field(default_factory=set)



def _check_against_file(files: str, file_parser: FileFilter, dirpath: str) -> tuple[str | None, str | None]:
    """
    Returns the create type and path that should be outputted
    Returns none if the file was excluded by regex
    WARNING: Rates being excluded as the highest priority
    So if a file matching a excluded regex or type, it will never be added as a base64 file even if it matches a type or a regex
    """
    _, extension = os.path.splitext(files)
    extension = extension[1:]
    if extension == "" and _.find(".") != -1: #Extra check for dotfiles as python can't figure em out
        extension = _[_.find(".")+1:]
    dont_exclude = extension not in file_parser.excluded_file_types and all(
        re.match(x, files) is None
        for x in file_parser.excluded_file_regex
    )

    if ( #Base64 Processed
        (file_parser.included_file_types is not None and extension in file_parser.included_file_types)
        or (file_parser.included_file_regex is not None and any(re.match(x, files) is not None for x in file_parser.included_file_regex))

    ) and dont_exclude:
        with open(dirpath + files, "rb") as reader:
            files += "|" + base64.b64encode(reader.read()).decode("utf-8")
        return "BASE64", files

    if dont_exclude:
        return "FILE", files
    return None, None

def _check_against_folder(directory: str, file_parser: FileFilter, dirpath: str) -> tuple[str | None, str | None]:
    """
    Returns the create type and path that should be outputted
    Returns None if the folder is excluded by the given folder regex
    Returns an empty string if the directory has files in it.
    ^
    This is used to save the output of the folder until we walk into it
    """
    if any(
        re.match(x, directory) is not None
        for x in file_parser.excluded_folder_regex
    ):

        return None, None

    if len(os.listdir(dirpath + directory)) == 0:
        return"FOLDER", directory

    return "", None

def _yield_files(file_parser: FileFilter, indent_real: str):
    "Create files then directories for yield"
    held_back: set[str] = set()
    dont_attend: set[str] = set() #Fill this with bad paths and do checks against path name
    indent = 0
    for dirpath, subdir, filenames in os.walk(".",  topdown=True):
        indent = dirpath.count(os.sep)
        log_dirpath = dirpath[2:]
        if any(x in dirpath for x in dont_attend):
            continue
        if dirpath in held_back:
            held_back.remove(dirpath)
            yield str(indent_real * (indent - 1)), "FOLDER", dirpath.split(os.sep)[-1], log_dirpath
        dirpath += os.sep
        for files in filenames:
            create_type, output = _check_against_file(files=files, file_parser=file_parser, dirpath=dirpath)
            if create_type is not None:
                yield str(indent_real * indent), create_type, output, log_dirpath + os.sep + files

        for directory in subdir:
            create_type, output = _check_against_folder(directory=directory, file_parser=file_parser, dirpath=dirpath)
            if create_type is None:
                dont_attend.add(dirpath + directory)
            elif output is None:
                held_back.add(dirpath + directory)
            else:
                yield str(indent_real * indent), create_type, output, log_dirpath + os.sep + directory


class DebugOpen():
    "This class exists to over open for debug purposes"
    def __init__(self, *args, **kwargs) -> None:
        pass
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    def write(self, string: str):
        "This class exists to over open for debug purposes"
    def close(self):
        "This class exists to over open for debug purposes"



def _gen_method(debug: bool, filename: str):
    if debug:
        return DebugOpen()
    return open(filename, "w+", encoding="utf-8" )


def lint_generate_file(filename: str, prefixs: dict[str,str], file_parser: FileFilter, indent_real: str, debug: bool):
    """Create a file thats hold a directory structure that can be remade on someone else's computer

    Args:
        filename (str): What file to output to
        prefixs (dict[str,str]): What prefix's to use for each item
        file_parser (FileFilter): Holds all information regarding excluding folders and files, and creating base64 files
        indent_real (str): The indent to use when indenting. This must be a representation of an actually indent EX: 4 spaces "    "
    """
    assert len(prefixs) == 3, "New file type added please edit _check_against_*"

    directory_file = _gen_method(debug, filename)

    directory_file.write("//Original Directory Name:" + os.getcwd().split(os.sep)[-1] +"\n")
    for indent, item_type, item, log_item in _yield_files(file_parser, indent_real):
        directory_file.write(indent + prefixs[item_type] + item +"\n")
        LOGGER.info(item_type + ": " + log_item)
    directory_file.close()
