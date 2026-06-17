"""
    bracketSeparator.py

    Adds a newline to the file where a ">" is located
    Uses command line arguments
"""

import os
import glob
from sys import argv

def separateBrackets(file: str, in_dir: str, out_dir: str):
    inputPath = str(in_dir + file)
    outputPath = str(out_dir + file)

    if os.path.isfile(inputPath):
        with open(inputPath, "r") as input:
            with open(outputPath, "w") as output:
                for line in input:
                    for char in line:
                        output.write(( ">\n") if char == ">" else char)
    else:
        print(f"Could not find \"{file}\" in \"{in_dir}\"")

# importlib execution
def main(*args):

    in_dir: str = args[0]
    out_dir: str = args[1]
    leng: int = len(args)

    if leng < 3:
        for img in glob.glob(str(in_dir + '*.txt')):
            separateBrackets(img[len(in_dir):], in_dir, out_dir)
    else:
        i: int = 2
        while i < leng:
            separateBrackets(args[i], in_dir, out_dir)
            i += 1

# regular execution
if __name__ == "__main__":

    in_dir : str = "input/"
    out_dir : str = "output/"
    loopfor : int = len(argv) - 1
    if loopfor < 1:
        for img in glob.glob(str(in_dir + '*.txt')):
            separateBrackets(img[len(in_dir):], in_dir, out_dir)
    else:
        i : int = 1
        while i < loopfor + 1:
            separateBrackets(argv[i], in_dir, out_dir)
            i += 1
