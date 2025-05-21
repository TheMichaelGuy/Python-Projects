"""
    bracketSeparator.py

    Adds a newline to the file where a ">" is located
    Uses command line arguments
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

        if os.path.isfile(inputPath):
            with open(inputPath, "r") as input:
                with open(outputPath, "w") as output:
                    for line in input:
                        for char in line:
                            output.write(( ">\n") if char == ">" else char)
        else:
            print(f"Could not find \"{sys.argv[i]}\" in \"{in_dir}\"")
        i += 1
