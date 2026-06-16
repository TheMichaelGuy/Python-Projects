"""
    svgFullColor.py

    Hopefully a whole Scratch SVG sprite the color decided by command line argument 1
"""

import os
from sys import argv
import glob

def full_color_svg(file: str, in_dir: str, out_dir: str, newColor: str):
    inputPath = str(in_dir + file)
    outputPath = str(out_dir + file)

    if os.path.isfile(inputPath):
        with open(inputPath, "r") as input:
            document = input.read()
        with open(outputPath, "w") as output:
            startIndex = stopIndex = 0

            while stopIndex != -1:
                stopIndex = document.find('="#', startIndex)

                if stopIndex != -1:
                    output.write(str(document[startIndex:stopIndex] + '="#' + newColor))
                    startIndex = stopIndex + 9
                else:
                    output.write(str(document[startIndex:]))

    else:
        print(f"Could not find \"{file}\" in \"{in_dir}\"")
    return

# importlib execution
def main(*args):

    in_dir: str = args[0]
    out_dir: str = args[1]
    leng: int = len(args)
    newColor: str = input("Enter Hexcode Color: ")
    if newColor.find("#") != -1:
        newColor = newColor[1:]

    if leng < 3:
        for img in glob.glob(str(in_dir + '*.svg')):
            full_color_svg(img[len(in_dir):], in_dir, out_dir, newColor)
    else:
        i: int = 2
        while i < leng:
            full_color_svg(args[i], in_dir, out_dir, newColor)
            i += 1

# regular execution
if __name__ == "__main__":

    in_dir: str = "input/"
    out_dir: str = "output/"
    loopfor: int = len(argv) - 1

    if loopfor < 1:
        print("No command line arguments. Making a dark copy of all sprites")
        newColor = "000000"
    else:
        newColor = str(argv[1])
        if newColor.find("#") != -1:
            newColor = newColor[1:]

    if loopfor < 2:
        for img in glob.glob(str(in_dir + '*.svg')):
            full_color_svg(img[len(in_dir):], in_dir, out_dir, newColor)
    else:
        i: int = 2
        while i < loopfor + 1:
            full_color_svg(argv[i], in_dir, out_dir, newColor)
            i += 1
