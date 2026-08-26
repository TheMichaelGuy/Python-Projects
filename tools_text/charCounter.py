"""
    charCounter.py

    Output a csv of the chars present for each entry in a list of strings
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
                    table : dict = {
                        "a": [],
                        "b": [],
                        "c": [],
                        "f": [],
                        "g": []
                    }
                    for char in table:
                        output.write(char + ",")
                    output.write("\n")

                    for i, line in enumerate(input):
                        
                        for char in table:
                            table[char].append(0)

                        
                        for char in line:
                            if char in table:
                                table[char][i] += 1

                        for char in table:
                            output.write(str(table[char][i]) + ",")
                        output.write("\n")


                    print(table)


                            
        else:
            print(f"Could not find \"{sys.argv[i]}\" in \"{in_dir}\"")
        i += 1