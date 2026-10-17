"""



"""

from sys import argv
from glob import glob
import os

# forces a yes or no answer
def input_validation(input: str):
    input = input.capitalize()
    if input in ["1", "Y", "YES"]:
        return True
    return False

# my function
def function(file: str, in_dir: str, out_dir: str):
    pass

# importlib execution
def main(*args):

    in_dir: str = args[0]
    out_dir: str = args[1]
    leng: int = len(args)

    if leng < 3:
        for img in glob(str(in_dir + '*.svg')):
            function(img[len(in_dir):], in_dir, out_dir)
    else:
        i: int = 2
        while i < leng:
            function(args[i], in_dir, out_dir)
            i += 1

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