"""Creates hard links of files.
Originally made for handbrake since handbrake doesn't go more than one level.
"""

import logging
import os
import sys
import time
from argparse import ArgumentParser, ArgumentTypeError
from typing import Iterable
import re
from itertools import zip_longest

from colorama import Fore, Style, init
import win32file

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


#Set up recycle bool
RECYCLE = False

#Set up colorama
init(autoreset=True, convert=True)

class HelpOutputParser(ArgumentParser):
    """This class exists to overwrite the error class in arg parse, so that help will print on all errors
    """
    def error(self, message):
        if len(sys.argv) != 1: # An argument was passed in
            message = message.split(":")
            front_mess = message[0]
            back_mess = ":".join(message[1:]) if len(message) > 1 else ""
            sys.stderr.write(f'{Fore.RED}ERROR: {front_mess}:{Style.RESET_ALL}{back_mess}\n\n')
        self.print_help(sys.stderr)
        sys.exit(2)

class Str2(str):
    """
    This class only exists to be able to check against whats returned in create_path.
    This way i don't have to do any fancy character inserts or something when returned.
    """



def create_path(path: str) -> str:
    """Creates a directory if not already a directory

    Args:
        path (str): the path to a directory

    Returns:
        str: The real path of the given string
    """
    if not os.path.isdir(path):
        return Str2(path)
    return os.path.realpath(path)

def dir_path(path: str) -> str:
    """Checks to the string is a real directory

    Args:
        path (str): the path to a directory

    Raises:
        ArgumentTypeError: If the input is not a directory

    Returns:
        str: The real path of the given string
    """
    if os.path.isdir(path):
        return os.path.realpath(path)
    raise ArgumentTypeError(f"readable_dir: \"{path}\" is not a valid path")




def _get_link_files(filenames: list[str], filetypes: list[str], regex: set[re.Pattern]):
    for files in filenames:
        for file_type, regex_pattern in zip_longest(filetypes, regex, fillvalue="a^"): #Import zip longest and combine file_types and check file_types then check regex
            if files.endswith(file_type) or re.match(regex_pattern, files) is not None:
                yield files
                # list_of_files.append((dirpath + os.sep + files, output_folder + os.sep + files))
                break

def create_hardlinks_filetypes(filetypes: list[str], regex: set[re.Pattern], output_folder: str, input_folder: str = ".", suppression: bool = False): # sourcery no-metrics
    """Create hardlinks of filetypes at output directory from input directory.

    Args:
        filetypes (Iterable): The filetypes to look for
        output_folder (str): The folder to create the hardlinks at
        input_folder (str, optional): The path to walk through to look for files that make [filetypes]. Defaults to "." which means where it was run from.
        verbosity (bool, optional): If every file copied should be outputted. Defaults to False.
    """
    list_of_files: list[tuple[str, str]] = []

    for dirpath, _, filenames in os.walk(input_folder):
        list_of_files.extend((dirpath + os.sep + files, output_folder + os.sep + files) for files in _get_link_files(filenames=filenames, filetypes=filetypes, regex=regex))
        # _get_link_files(filenames, filetypes, dirpath, output_folder, list_of_files)

    LOGGER.info("%s",f"Found {len(list_of_files)} files that match type{'s' if len(filetypes) > 1 else ''} {filetypes}")
    LOGGER.info("%s","Creating links for all files")

    error = 0


    for i in list_of_files:
        LOGGER.info("%s", "Attempting to link file: " + i[0])
        try:
            os.link(i[0], i[1])
        except FileExistsError:
            error += 1
            if not suppression:
                LOGGER.error("%s", Fore.RED + "ERROR: File " + Style.RESET_ALL + "\"" +  i[0] + "\"" +  Fore.RED + " already exists, Skipping file")
            LOGGER.error("Failed to link: %s", i[0])

    outtie = len(list_of_files) - error
    print(f"Found {len(list_of_files)} files that matched {filetypes}")
    print(f"Made hard links to {outtie} file{'' if outtie == 1 else 's'}")
    print(f"Failed {error} file{'' if outtie == 1 else 's'}")


def _remove_recycle(local: str):
    return not local.startswith("\\$Recycle")

def _walk_down(directory:str, file_types: Iterable, regex: set[re.Pattern]) -> tuple[int, list]:
    global RECYCLE
    deleted_files = []
    removal = 0
    for dirpath, _, filenames in os.walk(directory):
        for file_name in filenames:
            for file_type, regex_pattern in zip_longest(file_types, regex, fillvalue="a^"): #Import zip longest and combine file_types and check file_types then check regex
                if (file_name.endswith(file_type) or re.match(regex_pattern, file_name) is not None) and os.stat(dirpath + os.sep + file_name).st_nlink > 1:
                    if (
                        RECYCLE and len(list(filter(_remove_recycle, win32file.FindFileNames(dirpath + os.sep + file_name)
                            )
                        ))
                        == 1
                    ):
                        break
                    removal += 1
                    os.remove(dirpath + os.sep + file_name)
                    deleted_files.append(dirpath + os.sep + file_name)
                    break
    return removal, deleted_files


def _directory_cleanup(directory:str, file_types: Iterable, regex: set[re.Pattern]) -> tuple[int, list]:
    removal = 0
    deleted_files = []
    for file_name in os.listdir(directory):
        for file_type, regex_pattern in zip_longest(file_types, regex, fillvalue="a^"): #Import zip longest and combine file_types and check file_types then check regex
            if (file_name.endswith(file_type) or re.match(regex_pattern, file_name) is not None) and os.stat(directory + os.sep + file_name).st_nlink > 1: #Has to be in brackets
                if (
                    RECYCLE and len(list(filter(_remove_recycle, win32file.FindFileNames(directory + os.sep + file_name)))
                    )
                    == 1
                ):
                    break
                removal += 1
                os.remove(directory + os.sep + file_name)
                deleted_files.append(directory+ os.sep + file_name)
                break
    return removal, deleted_files

def cleanup_hardlinks(directory:str, file_types: Iterable, regex: set[re.Pattern], walkdown: bool = False):
    """Use to remove hard links from a directory
    WARNING: Windows does not differentiate between the hard linked file and the original.
    If walkdown is true, it will go through all folders and remove any files who are part of a link whether it's the original or linked.

    Args:
        directory (str): The directory to look for files in
        file_types (Iterable): The kinds of files to check for links
        walkdown (bool, optional): Walks through all directories in given location rather than only searching the first. Defaults to False.
        log (bool, optional): Whether or not to create a log of deleted files. Defaults to False.
        verbosity (bool, optional): Output all deleted files to the console. Defaults to False.
    """

    if walkdown:
        removal, deleted_files = _walk_down(directory, file_types, regex)
    else:
        removal, deleted_files = _directory_cleanup(directory, file_types, regex)

    for output_line in deleted_files:
        LOGGER.info("Removed: %s", output_line)
    if not deleted_files:
        LOGGER.info("No hard linked files found")

    print(f"Found and removed {removal} file{'' if removal == 1 else 's'} that had more than 1 link to it.")



def main():
    "Main method for hard linking files"

    path = os.path.realpath(os.getcwd())
    parser = HelpOutputParser(description="Hardlink specific file types to a directory. Or clean hardlinks types")
    parser.add_argument("mode", type=lambda x:x.lower(), choices=["make", "clean"], help="Create hardlinks for file types or clean hardlinks. Cleaning hardlinks will always leave 1 copy of the file in the directory.")
    parser.add_argument("output", type=create_path, help="The directory that the file links should be outputted to." \
                        + "If the directory path doesn't exist it will create the directory.")
    parser.add_argument("filetypes", nargs="+", type=lambda x: x.lower(), action="extend", help="The filetypes being copied to the new folder") # Make file endings lower to match lower files
    parser.add_argument("-r", "--regex", nargs='+', type=re.compile, help="Add regex to check on files to hard link", default=set()) #Ad
    #Flags for hardlink function
    group = parser.add_argument_group("Hardlink creation specific flags")
    group.add_argument("-i", "--input", type=dir_path, help="The directory to start searching for files in. " \
                        +" If no input is given, it will start searching from the folder the program is ran from.", default=path)
    group.add_argument("-p", "--prompt", action="store_true", help="Prompts you before creating the output directory")
    group.add_argument("-s", "--suppress", action="store_true", help="Don't output file error's if they occur.")

    #Flags for cleaning function
    group = parser.add_argument_group("Hard link cleaning flags")
    group.add_argument("-w", "--walkdown", action="store_true", help="Walks through all directories under the given directory")
    group.add_argument("-ir", "--ignorerecyclingbin", action="store_true", help="Get list of hard links and and remove any links that are in the recycling bin before deciding to delete")

    #Flags for either function
    group = parser.add_argument_group("Flags that apply for both")
    group.add_argument('--verbose', '-v', action='store_true', help="Turn on verbosity to print each copied/deleted file")
    group.add_argument("-l", "--log", action="store_true", help="Send all errored/deleted files to a txt document outputted in the same directory.")

    args = parser.parse_args()
    if args.verbose: #We have to check verbosity first or else the removal of the color will affect the console output
        slh = logging.StreamHandler(sys.stdout)
        slh.setFormatter(FORMATTERSH)
        LOGGER.addHandler(slh)
    if args.log:
        flh = logging.FileHandler(filename=args.output + os.sep + f"DELETED_HARD_LINKS{time.strftime('_%H_%M_%d_%m_%Y')}.log", mode='w')
        flh.setFormatter(FORMATTERFH)
        LOGGER.addHandler(flh)
    global RECYCLE
    RECYCLE = args.ignorerecyclingbin
    args.regex = set(args.regex)
    if args.mode == "clean":
        if isinstance(args.output, Str2):
            print(f"Directory {args.output} does not exist, thus cannot be cleaned.")
            sys.exit(0)


        cleanup_hardlinks(directory=args.output, file_types=args.filetypes, walkdown=args.walkdown, regex=args.regex)

    else:
        if isinstance(args.output, Str2): #We check to see if it is specificity this class, thus letting us know we need to create the directory
            if args.prompt: #Prompt is here just in case. I remember it from other cmdline tools, so i added it
                if input(f"Directory {args.output} does not exist. Would you like to create it(y or yes)?: ").lower() in ["y", "ye", "yes"]:
                    print(f"Created directory(s) {args.output}.")
                    os.makedirs(args.output)
                    args.output = os.path.realpath(args.output)
                else:
                    print("Directory not created. Exiting program.")
                    sys.exit(0)
            else:
                os.makedirs(args.output)
                args.output = os.path.realpath(args.output)

        create_hardlinks_filetypes(filetypes=args.filetypes, output_folder=args.output, input_folder=args.input, suppression=args.suppress, regex=args.regex)

if __name__ == "__main__":
    main()
