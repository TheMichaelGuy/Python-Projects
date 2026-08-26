"""
rEdgeCopy.py

Copies the selected file(s) into the edges of a directory tree
"""

from sys import argv
import os

# forces a yes or no answer
def input_validation(input: str):
    input = input.capitalize()
    if input in ["1", "Y", "YES"]:
        return True
    return False

# saves a input file of an extension as an output file of another extension
def save_as(input_file: str, output_file: str):
    with open(input_file, "rb") as input:
        with open(output_file, "wb") as output:
            output.write(input.read())

# out_dir will be ignored
def function(export_method, **kwargs):
    in_dir: str = kwargs.get("in_dir", "")

    # find all ending directories
    walkies = os.walk(in_dir)
    for root, d_names, f_names in walkies:
        #print(f"root: {root}, d_names{d_names} f_names{f_names}")
        # at the edge of a directory
        if len(d_names) == 0:
            # handle the copying process to reduce redundancy
            export_method(root, **kwargs)

# separating the logic to remove redundancy
def exporter_all(root: str, **kwargs):

    #print("exporter_all")
    in_dir: str = kwargs.get("in_dir", "")
    name_after_dir: bool = kwargs.get("name_after_dir", False)
    do_override: bool = kwargs.get("do_override", False)

    # grab first file_list from iterator
    walkies = os.walk(in_dir) # this is potentially redundant
    for _, _, files in walkies:
        #print(f"f_names{files}")
        break

    for file in files:
        #print(f"got file {file}")
        #out_name: str = os.path.basename(file)
        if do_override:
            if name_after_dir:
                #print(1)
                folder_name: str = os.path.basename(root)
                extension: str = os.path.splitext(os.path.basename(file))[1]

                output_file: str = root + "/" + folder_name + extension

                save_as(file, output_file)
                #print("Only the first file can be copied")
                break
            else:
                #print(2)
                save_as(file, root + "/" + os.path.basename(file))

        else:

            if name_after_dir:
                
                #print(3)
                folder_name: str = os.path.basename(root)
                extension: str = os.path.splitext(os.path.basename(file))[1]

                #print(f"extension {extension}")
                output_file: str = root + "/" + folder_name + extension
                #print(f"output_file {output_file}")

                if not os.path.isfile(output_file):
                    save_as(file, output_file)
                    #print("Only the first valid file can be copied")
                    break
            else:
                #print(4)
                output_file: str = root + "/" + os.path.basename(file)
                if not os.path.isfile(output_file):
                    save_as(file, output_file)

# separating the logic to remove redundancy
def exporter_args(root: str, **kwargs):

    #print("exporter_args")
    in_dir: str = kwargs.get("in_dir", "input/")
    name_after_dir: bool = kwargs.get("name_after_dir", False)
    do_override: bool = kwargs.get("do_override", False)

    # grab args
    argv = kwargs.get("argv", [])
    leng: int = len(argv)

    if leng < 3:
        print("Not enough args")
        exit(1)

    i: int = 2

    if do_override:
        if name_after_dir:
            #print(1)
            while i < leng:
                input_file: str = in_dir + "/" + argv[i]

                folder_name: str = os.path.basename(root)
                extension: str = os.path.splitext(os.path.basename(input_file))[1]

                output_file: str = root + "/" + folder_name + extension

                save_as(input_file, output_file)
                #i += 1
                break
        else:
            #print(2)
            while i < leng:
                input_file: str = in_dir + "/" + argv[i]
                output_file: str = root + "/" + os.path.basename(input_file)

                save_as(input_file, output_file)
                i += 1
    else:
        if name_after_dir:
            #print(3)
            while i < leng:
                input_file: str = in_dir + "/" + argv[i]

                folder_name: str = os.path.basename(root)
                extension: str = os.path.splitext(os.path.basename(input_file))[1]

                output_file: str = root + "/" + folder_name + extension

                save_as(input_file, output_file)
                #i += 1
                break
        else:
            #print(4)
            while i < leng:
                input_file: str = in_dir + "/" + argv[i]
                output_file: str = root + "/" + os.path.basename(input_file)

                save_as(input_file, output_file)
                i += 1    

# importlib execution
def main(*args):

    in_dir: str = args[0]
    #out_dir: str = args[1]
    leng: int = len(args)

    # This would only work for one file
    name_after_dir: bool = input_validation(input("Should the copied files be the same name as each directory? (Only one file will be copied) (y/n): "))
    # This can work for multiple files
    do_override: bool = input_validation(input("Should the copied file overwrite an already present file? (y/n): "))

    if leng < 3:
        function(export_method=exporter_all, in_dir=in_dir, name_after_dir=name_after_dir, do_override=do_override)
    else:
        function(export_method=exporter_args, in_dir=in_dir, name_after_dir=name_after_dir, do_override=do_override, argv=args)

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