"""
    tidyTextFile.py

    Removes trailing whitespace in a document, removes extra newlines in a file, and ends a file with a newline
    INPUT: Name of file from input directory to clean up
    OUTPUT: The cleaned up file is sent to the output directory
"""

import os
import sys

in_dir : str = "input/"
out_dir : str = "output/"
loopfor : int = len(sys.argv) - 1
if loopfor < 1:
    print("No command line arguments")
else:
    i : int = 1
    while i < loopfor + 1:
        inputPath = str(in_dir + sys.argv[i])
        outputPath = str(out_dir + sys.argv[i])
        #print(sys.argv[i])
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
            print(f"Could not find \"{sys.argv[i]}\" in \"{in_dir}\"")
        i += 1
