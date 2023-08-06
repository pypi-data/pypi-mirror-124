# HardLinks

Made for handbrake like programs that don't walk all sub directories in a folder, hard links all given file types to a given directory

# Installation
Install through pip:

    python3 -m pip install HardLinks

# Documentation

### Creating Hard Links

To create hard links needs 2 things to function:
    1. The directory to output the files to. It will create the folder if it does not exist
    2. The file types


So creating hard links for mkv and mp4's look like:

    hardlinks create path\to\directory mkv mp4

This will make the new folder and add all hard links to it.

HardLinks will start searching from the directory it was run from. To change this, us the -i switch with the path:

    hardlink create . mkv mp4 -i path\to\files

Other creation flags:
    * -p will ask you before creating the folder
    * -s will not show file errors in the output

### Removing Hard links

To clean hard links needs 2 things to function:
    1. The directory to clean
    2. The file types

While a hard link can be removed by deleting, you can also remove it by using the clean arg:

    hardlink clean . mkv mp4

By default it only cleans the directory it was run in. Use the -w to walk through all sub directories. This will leave a copy of the file within the walk as long as the file doesn't exist anywhere else. The recycling bin is also counted in existence.

    hardlink clean . mkv mp4 -w


WARNING: Do not combine the 2 methods. If you use -w or run the program in the original directory of the file, it will still delete the file due to the number of links being > 1. To avoid this, use the -ir switch

    hardlink clean . mkv mp4 -ir

This will check to see how many links are in the bin and remove them from the count. It will then not delete the original file.


### Misc

You can also pass in regex using the -r, so files can be checked for names rather than extensions. This accept multiple regex:

    hardlink clean . mkv -r ".*dog.*" ".*angels.*"
    hardlink make . mkv -r ".*dog.*"

This method still require's a file extension, but can be filled with anything, so use a nonexistent file type in the search directory

    hardlink clean . thiswillmakenothing -r ".*dog.*"

Turn on logging and verbosity with -v and -l