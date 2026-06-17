"""
    tidyTextFile.py

    Removes trailing whitespace in documents, removes large newline gaps, and ends files with a newline
    INPUT: Names of files from input directory to clean up
    OUTPUT: The cleaned up files are sent to the output directory
"""

import os
import glob
from sys import argv

def tidy_text(file: str, in_dir: str, out_dir: str):
    inputPath = str(in_dir + file)
    outputPath = str(out_dir + file)
    #print(file)
    if os.path.isfile(inputPath):
        newlineGap : bool = False
        with open(inputPath, "r") as input:
            with open(outputPath, "w") as output:
                for line in input:
                    if (newlineGap and line != '\n'):
                        newlineGap = False # check for repeat newline gap first
                    if not(newlineGap and line == '\n'):
                        output.write(line.rstrip() + '\n') # stripping trailing whitespace and guaranteeing a newline
                    if (line == '\n'):
                        newlineGap = True # only allow a gap of a single newline

    else:
        print(f"Could not find \"{file}\" in \"{in_dir}\"")

# importlib execution
def main(*args):

    in_dir: str = args[0]
    out_dir: str = args[1]
    leng: int = len(args)

    if leng < 3:
        for img in glob.glob(str(in_dir + '*.txt')):
            tidy_text(img[len(in_dir):], in_dir, out_dir)
    else:
        i: int = 2
        while i < leng:
            tidy_text(args[i], in_dir, out_dir)
            i += 1

# regular execution
if __name__ == "__main__":

    in_dir : str = "input/"
    out_dir : str = "output/"
    loopfor : int = len(argv) - 1

    if loopfor < 1:
        for img in glob.glob(str(in_dir + '*.txt')):
            tidy_text(img[len(in_dir):], in_dir, out_dir)
    else:
        i : int = 1
        while i < loopfor + 1:
            tidy_text(argv[i], in_dir, out_dir)
            i += 1
