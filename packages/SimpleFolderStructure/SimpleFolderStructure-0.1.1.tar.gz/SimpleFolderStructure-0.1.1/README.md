# SimpleFolderStructure - Save and create directories from a file

SimpleFolderStructure allows you to save and share directory structure's from a txt file. It' allows 
* Save file contents as base64, then have the contents copied when created
* Choose which files using regex or types
* Exclude files and folders using regex or types
* Custom indent size and characters
* Custom prefix's for each type of files

# Installation
Install through pip:

    python3 -m pip install SimpleFolderStructure
    
# Documentation

### Saving structure's 
To use SimpleFolderStructure, navigate to the directory you want to copy and start the script using:

    folderstructure save "Outputfile.txt"
    
This will create a script that will output your current directory in a format like so:

```
#Outputfile.txt
: afileinthestartdirectory.bat
: grandmascookies.docx
* DirectoryBelowMain
    : afileinthatdirectory.py
    : anotherone.txt
* AnotherDirectory
    : randomfile.js
```

Using -intype or -inregex, any matches content will be encoded to base64 and placed on the same line. When they are created, they will share the same content:

```
folderstructure save "Outputfile.txt" -intype txt -inrex ".*that.*"
#Outputfile.txt
: afileinthestartdirectory.bat
: grandmascookies.docx
* DirectoryBelowMain
    ? afileinthatdirectory.py|cHJpbnQoIkEgYmFzZSA2NCBlbmNvZGVkIHB5dGhvbiBmaWxlISIp
    ? anotherone.txt|RHVjaw==
* AnotherDirectory
    : randomfile.js
```

Adding -extype or -exrex, any matches will be excluded from the output. This will nullify if the file was included within the -intype or -inrex:
```
folderstructure save "Outputfile.txt" -extype bat docx
#Outputfile.txt
* DirectoryBelowMain
    : afileinthatdirectory.py
    : anotherone.txt
* AnotherDirectory
    : randomfile.js
```
Adding -exfold will remove folders that match the regex. This will remove entire path's meaning any files after will be removed too:
```
folderstructure save "Outputfile.txt" -exfold .*Another.*
#Outputfile.txt
: afileinthestartdirectory.bat
: grandmascookies.docx
* DirectoryBelowMain
    : afileinthatdirectory.py
    : anotherone.txt
```

#### NOTE: Excludes are done before includes, so if a file is found to be excluded it will not add it even if included by type or regex
### Creating structures from files
To create a structure, input create and the file to use to make it:

    folderstructure create "Outputfile.txt"

This will create all files, not overriding existing ones.

    Created 3 files, 1 file already existed.

### Editing output style
Using -s and -c you can make the characters and size of the indent different to create a different look

```
folderstructure save "Outputfile.txt" -s 3 -c *
#3 * per indent
#Outputfile.txt
: afileinthestartdirectory.bat
: grandmascookies.docx
* DirectoryBelowMain
***: afileinthatdirectory.py
***: anotherone.txt|RHVjaw==
* AnotherDirectory
***: randomfile.js
```

Character can be any length and will repeat the number of times given to size
```
folderstructure save "Outputfile.txt" -s 2 -c #@
# 2 sets of #@ per indent
#Outputfile.txt
: afileinthestartdirectory.bat
: grandmascookies.docx
* DirectoryBelowMain
#@#@: afileinthatdirectory.py
#@#@: anotherone.txt
* AnotherDirectory
#@#@: randomfile.js
```

### Prefix's
While prefix customization exists, the characters used for a prefix are characters that are not allowed in windows files. Please be careful when changing them, as changing them could result in error's. Prefix's checks are done in alphabetical order, so if a base64 prefix is in a name, it will find it first

EX:
Setting the BASE64 prefix to yB would make '* DirectoryBelowMain' a BASE64 file. It will not cause an error as list slicing cannot produce an error
    
# TODO's
* [ ] Config file to avoid long command line arguments
- [ ] Input for directory or file names. 
- Directory: (Name for directory) ask's for a name in the cmdline before creating a file
- File: (Name for main script|py) will create a file with input from the cmdline with the extension py
* [ ] Base64 files to let user's enter text from the cmdline. 
* This could be useful for package name and consolescript name when creating setup.py.
- [ ] Allow for creation of variables while creating files to avoid multiple repeated entries




