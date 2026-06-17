"""
    main.py

    A messy Python script to run other Python scripts
    Add a bash alias to run this from anywhere
"""

import os

from importlib import import_module
from shlex import split
from sys import argv

def validate_loop(input_str : str, in_dir : str, out_dir : str):
    if input_str in ["exit", "q"]:
        return "exit"
    if input_str in ["list", "help"]:
        list_tools()
        return "list"
    if input_str == "input":
        in_dir = input("Enter a relative input directory: ")
        if not in_dir.endswith("/"):
            in_dir = in_dir + "/"
        return "in"
    if input_str == "output":
        out_dir = input("Enter a relative output directory: ")
        if not out_dir.endswith("/"):
            out_dir = out_dir + "/"
        return "out"
    else:
        return "exec"

# List the available tools in additional directories
def list_tools():
    main_location : str = os.path.dirname(os.path.abspath(__file__)) # Used for locating tool directories
    for folder in next(os.walk(main_location))[1]:
        tools : list[str] = [f[:-3] for f in os.listdir(main_location + "/" + folder) if f.endswith(".py") and f != "__init__.py"]
        if tools:
            print(folder)
            for tool in tools:
                print(f"\t{tool}")

# Find the folder that contains the tool you want to use
def find_folder(main_location: str, tool: str):
    for fldr in next(os.walk(main_location))[1]:
        for f in os.listdir(main_location + "/" + fldr):
            if f == tool:
                return fldr
    return ""

# main
if __name__ == "__main__":

    # Relative input and output paths
    in_dir : str = ""
    out_dir : str = "output/"

    # Get file locations
    current_location : str = os.getcwd() # Used for input and output
    main_location : str = os.path.dirname(os.path.abspath(__file__)) # Used for locating tool directories
    # Check for argv and attempt to run that instead
    #print(argv)
    if len(argv) > 1:
        #print("Shortcut!")
        argv[1]
        folder : str = find_folder(main_location, argv[1])
        if folder != "":
            try:
                module = import_module(f"{folder}.{argv[1][:-3]}") # Note that this will run the outer code first, so everything should go in main from now on
                if hasattr(module, "main"):
                    argv.pop(0) # Remove command
                    argv.pop(0)
                    argv.insert(0, current_location + "/" + in_dir)
                    out_path : str = current_location + "/" + out_dir
                    argv.insert(1, out_path)
                    #print(f"args {argv}")
                    if not os.path.exists(out_path):
                        os.makedirs(out_path)
                    module.main(*argv) # each main will have to accept in_dir and out_dir as args and prompt the user for the rest of the args that aren't files
                    exit()
                else:
                    print(f"Module {module} doesn't have main() function")
            except ModuleNotFoundError:
                print(f"Tool {argv[1]} not found... somehow")
        else:
            print("Couldn't find the tool!")

    # Input loop
    done : bool = False
    print("TheMichaelGuy's Collection of Python Scripts")
    print(f"Current Location: {current_location}")
    print(f"Location of main.py: {main_location}\n")
    while not done:
        input_str = input(">>> ")
        effect = validate_loop(input_str, in_dir, out_dir)
        if effect == "exit":
            done = True
        elif effect == "exec":
            args = split(input_str)
            if args[0] == "__init__.py" or not args[0].endswith(".py"):
                print("We can't run that file! (Script must end with \".py\" and not be \"__init__.py\")")
            else:
                folder : str = find_folder(main_location, args[0])
                if folder != "":
                    try:
                        module = import_module(f"{folder}.{args[0][:-3]}") # Note that this will run the outer code first, so everything should go in main from now on
                        if hasattr(module, "main"):
                            args.pop(0) # Remove command
                            args.insert(0, current_location + "/" + in_dir)
                            args.insert(1, current_location + "/" + out_dir)
                            #print(f"args {args}")
                            if not os.path.exists(out_path):
                                os.makedirs(out_path)
                            module.main(*args) # each main will have to accept in_dir and out_dir as args and prompt the user for the rest of the args that aren't files
                        else:
                            print(f"Module {module} doesn't have main() function")
                    except ModuleNotFoundError:
                        print(f"Tool {args[0]} failed with library imports")
                else:
                    print("Couldn't find the tool!")
