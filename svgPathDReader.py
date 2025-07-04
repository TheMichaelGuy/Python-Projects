"""
    svgPathDReader.py

    Reads an svg document and prints the commands for a d attribute in a path element
    in a more understandable way. It's better to use this for simple shapes since the
    output would get large.
"""

# For more info on d attributes: https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/d

import re
import os
import sys

def findFirstChar(string : str, substr : str, start : int, end : int):
    if len(string) < 1:
        return -1
    if start == None:
        start = 0
    if end == None:
        end = len(string)
    closestChar : str = None
    closestIndex : int = -1
    for char in substr:
        index = string.find(char, start, end)
        if (closestIndex == -1 or index < closestIndex) and index != -1:
            closestIndex = index
            closestChar = char

    return closestIndex, closestChar

def splitPathDCommands(dPathString : str):
    if dPathString == "":
        empty : list[list[str]] = []
        return empty
    startIndex : int = 0
    endIndex : int = len(dPathString) - 1
    indexes : list[int] = []
    commands : list[str] = []
    while startIndex != -1:
        startIndex, command = findFirstChar(dPathString, "MmLlHhVvCcSsQqTtAaZz", startIndex, endIndex)
        if startIndex != -1:
            indexes.append(startIndex + 1)
            commands.append(command)
            startIndex += 1
    
    if len(indexes) == 0:
        return []
    dPathCommands : list[list[str]] = []
    i = 0
    while i < len(indexes) - 1:
        dPathCommands.append([commands[i], dPathString[indexes[i]:indexes[i + 1] - 1]])
        i += 1
    if dPathString[-1] in "Zz":
        dPathCommands.append([commands[i], dPathString[indexes[i]:-1]])
        dPathCommands.append([dPathString[-1], ""])
    else:
        dPathCommands.append([commands[i], dPathString[indexes[i]:]])
    
    return dPathCommands

def processPathD(value : str):
    pathDCommands : list[list[str]] = splitPathDCommands(value)
    # isolate all numbers
    pathDNumbers = []
    for pair in pathDCommands:
        pathDNumbers.append([pair[0], re.split(",| ", pair[1])])
    #print(pathDNumbers)

    for pair in pathDNumbers:
        if pair[0] == "M":
            print(f"M: MoveTo x={pair[1][0]} y={pair[1][1]}")
        elif pair[0] == "m":
            print(f"m: MoveTo dx={pair[1][0]} dy={pair[1][1]}")
        elif pair[0] == "L":
            print(f"L: LineTo x={pair[1][0]} y={pair[1][1]}")
        elif pair[0] == "l":
            print(f"l: LineTo dx={pair[1][0]} dy={pair[1][1]}")
        elif pair[0] == "H":
            print(f"H: Horizontal LineTo x={pair[1][0]}")
        elif pair[0] == "h":
            print(f"h: Horizontal LineTo dx={pair[1][0]}")
        elif pair[0] == "V":
            print(f"V: Vertical LineTo y={pair[1][0]}")
        elif pair[0] == "v":
            print(f"v: Vertical LineTo dy={pair[1][0]}")
        elif pair[0] == "C":
            print(f"C: Cubic Bézier curve x1={pair[1][0]} y1={pair[1][1]} x2={pair[1][2]} y2={pair[1][3]} x={pair[1][4]} y={pair[1][5]}")
        elif pair[0] == "c":
            print(f"c: Cubic Bézier curve dx1={pair[1][0]} dy1={pair[1][1]} dx2={pair[1][2]} dy2={pair[1][3]} dx={pair[1][4]} dy={pair[1][5]}")
        elif pair[0] == "S":
            print(f"S: Reflective Cubic Bézier curve x2={pair[1][0]} y2={pair[1][1]} x={pair[1][2]} y={pair[1][3]}")
        elif pair[0] == "s":
            print(f"s: Reflective Cubic Bézier curve dx2={pair[1][0]} dy2={pair[1][1]} dx={pair[1][2]} dy={pair[1][3]}")
        elif pair[0] == "Q":
            print(f"Q: Quadratic Bézier curve x1={pair[1][0]} y2={pair[1][1]} x={pair[1][2]} y={pair[1][3]}")
        elif pair[0] == "q":
            print(f"q: Quadratic Bézier curve dx1={pair[1][0]} dy2={pair[1][1]} dx={pair[1][2]} dy={pair[1][3]}")
        elif pair[0] == "T":
            print(f"T: Reflective Quadratic Bézier curve x={pair[1][0]} y={pair[1][1]}")
        elif pair[0] == "t":
            print(f"t: Reflective Quadratic Bézier curve dx={pair[1][0]} dy={pair[1][1]}")
        elif pair[0] == "A":
            print(f"A: Elliptical arc curve rx={pair[1][0]} ry={pair[1][1]} angle={pair[1][2]} arc={pair[1][3]} x={pair[1][4]} y={pair[1][5]}")
        elif pair[0] == "a":
            print(f"A: Elliptical arc curve rx={pair[1][0]} ry={pair[1][1]} angle={pair[1][2]} arc={pair[1][3]} dx={pair[1][4]} dy={pair[1][5]}")
        elif pair[0] == "Z":
            print(f"Z: ClosePath")
        elif pair[0] == "z":
            print(f"z: ClosePath")
        else:
            print("Unknown Element")    

    return

in_dir : str = "input/"
out_dir : str = "output/"
loopfor : int = len(sys.argv)

if loopfor < 1:
    print("No command line arguments")
    exit

i : int = 1
while i < loopfor:
    inputPath = str(in_dir + sys.argv[i])
    outputPath = str(out_dir + sys.argv[i])

    j = 1
    if os.path.isfile(inputPath):
        with open(inputPath, "r") as input:
            document = input.read()
            
        startIndex = stopIndex = 0
        while startIndex != -1:

            startIndex = document.find("path d", startIndex)
            if startIndex != -1:
                stopIndex = document.find("\"", startIndex + 8)
                value : str = document[startIndex + 8: stopIndex]

                print(f"PATH {j}")
                processPathD(value)

                startIndex += 8
                j += 1

    else:
        print(f"Could not find \"{sys.argv[i]}\" in \"{in_dir}\"")
    i += 1
