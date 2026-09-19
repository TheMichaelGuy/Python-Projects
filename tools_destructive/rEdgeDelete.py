"""
rEdgeCopy.py

Deletes the selected file(s) of the edges of a directory tree
"""

from sys import argv
import os

# forces a yes or no answer
def input_validation(input: str):
    input = input.capitalize()
    if input in ["1", "Y", "YES"]:
        return True
    return False

# deletes a file
def delete_file(file: set, verbose: bool = True):
    if os.path.isfile(file):
        os.remove(file)
        if verbose:
            print("File has been deleted")
    elif verbose:
        print("File does not exist")

# out_dir will be ignored
def function(delete_method, **kwargs):
    in_dir: str = kwargs.get("in_dir", "")

    # find all ending directories
    walkies = os.walk(in_dir)
    for root, d_names, f_names in walkies:
        #print(f"root: {root}, d_names{d_names} f_names{f_names}")
        # at the edge of a directory
        if len(d_names) == 0:
            # handle the deleting process to reduce redundancy
            delete_method(root, **kwargs)

# separating the logic to remove redundancy
def deleter_all(root: str, **kwargs):

    in_dir: str = kwargs.get("in_dir", "")

    # grab first file_list from iterator
    walkies = os.walk(in_dir) # this is potentially redundant
    for _, _, files in walkies:
        #print(f"f_names{files}")
        break

    for file in files:
        delete_path: str = root + "/" + os.path.basename(file)
        #delete_file(file) # WRONG COMMAND WRONG COMMAND
        delete_file(delete_path)

# separating the logic to remove redundancy
def deleter_args(root: str, **kwargs):

    in_dir: str = kwargs.get("in_dir", "")
    # grab args
    argv = kwargs.get("argv", [])
    leng: int = len(argv)

    i: int = 2
    while i < leng:
        delete_path: str = root + "/" + os.path.basename(argv[i])
        #delete_file(in_dir + "/" + argv[i]) # WRONG COMMAND WRONG COMMAND
        delete_file(delete_path)
        i += 1

# importlib execution
def main(*args):

    in_dir: str = args[0]
    #out_dir: str = args[1]
    leng: int = len(args)

    ask1: bool = input_validation(input("This will delete every file in the edge of the file tree. Are you sure you want to continue? (y/n):"))
    if not ask1:
        print("exiting")
        exit(0)

    ask2: bool = input_validation(input("Are you REALLY sure you want to continue? Double-check the folder path (y/n):"))
    if not ask2:
        print("exiting")
        exit(0)

    if leng < 3:
        function(delete_method=deleter_all, in_dir=in_dir)
    else:
        function(delete_method=deleter_args, in_dir=in_dir, argv=args)

# regular execution
if __name__ == "__main__":

    in_dir: str = "input/"
    out_dir: str = "output/"
    current_location : str = os.getcwd()

    argv.pop(0)
    argv.insert(0, current_location + "/" + in_dir)
    out_path : str = current_location + "/" + out_dir

    argv.insert(1, out_path)
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    main(*argv)