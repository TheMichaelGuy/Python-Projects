"""
    svgReshapeBisector.py

    Takes an svg Document that uses the path element with d attributes and modifies said attributes
    so that certain commands are bisected into two commands.

    For now, this only works for l, h, v, c commands, perfect for Scratch vector objects
"""

#https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/d

# For c
# https://math.stackexchange.com/questions/3092244/how-to-perfectly-split-a-bezier-curve-into-two-curves-of-unequal-length
# https://en.wikipedia.org/wiki/Cubic_Hermite_spline#Representations

# https://pages.mtu.edu/~shene/COURSES/cs3621/NOTES/spline/Bezier/bezier-sub.html
# https://bezier.readthedocs.io/en/stable/python/reference/bezier.curve.html

import re
import os
import sys
import glob

import bezier # pip install bezier
import numpy as np

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

def bisectPathD(value : str):
    pathDCommands : list[list[str]] = splitPathDCommands(value)
    # isolate all numbers
    pathDNumbers = []
    for pair in pathDCommands:
        pathDNumbers.append([pair[0], re.split(",| ", pair[1])])

    newStrings : list[str] = []
    for pair in pathDNumbers:
        if pair[0] in "lhv":
            parameterSet : str = ""
            delimiterBit : bool = False
            isFirst : bool = True
            for num in pair[1]:
                num = float(num) / 2
                if isFirst:
                    parameterSet += str(num)
                    isFirst = False
                elif delimiterBit:
                    parameterSet += (" " + str(num))
                    delimiterBit = False
                else:
                    parameterSet += ("," + str(num))
                    delimiterBit = True
            newStrings.append(pair[0] + parameterSet)
            newStrings.append(pair[0] + parameterSet)
        if pair[0] in "c":
            nodes = np.asfortranarray([
                [0.0, float(pair[1][0]), float(pair[1][2]), float(pair[1][4])],
                [0.0, float(pair[1][1]), float(pair[1][3]), float(pair[1][5])]
            ])
            curve = bezier.Curve(nodes, degree=3)
            left, right = curve.subdivide()
            lx, ly = left.nodes
            rx, ry = right.nodes
            #print(f"lx {lx}, ly {ly}, rx {rx}, ry {ry}")
            newStrings.append("c" + str(lx[1]) + "," + str(ly[1]) + " " + str(lx[2]) + "," + str(ly[2]) + " " + str(lx[3]) + "," + str(ly[3]))
            newStrings.append("c" + str(rx[1] - lx[3]) + "," + str(ry[1] - ly[3]) + " " + str(rx[2] - lx[3]) + "," + str(ry[2] - ly[3]) + " " + str(rx[3] - lx[3]) + "," + str(ry[3] - ly[3]))
        if pair[0] in "MmLTtCSsHVQq": # Coordinate Variables
            parameterSet : str = ""
            delimiterBit : bool = False
            isFirst : bool = True
            for num in pair[1]:
                if isFirst:
                    parameterSet += str(num)
                    isFirst = False
                elif delimiterBit:
                    parameterSet += (" " + str(num))
                    delimiterBit = False
                else:
                    parameterSet += ("," + str(num))
                    delimiterBit = True
            newStrings.append(pair[0] + parameterSet)

        if pair[0] in "Aa": # Elliptical Arc Curve
            newStrings.append(str(pair[0]) + " " + str(pair[1][0]) + " " + str(pair[1][1]) + " " + str(pair[1][2]) + " " + str(pair[1][3]) + " " + str(pair[1][4]) + " " + str(pair[1][5]) + "," + str(pair[1][6]))
        if pair[0] in "Zz": # 0 vars
            newStrings.append(str(pair[0]))

    finalString : str = ""
    for func in newStrings:
        finalString += func
    return finalString

def bisectSVG(file : str, in_dir : str, out_dir : str):
    inputPath = str(in_dir + file)
    outputPath = str(out_dir + file)

    if os.path.isfile(inputPath):
        with open(inputPath, "r") as input:
            document = input.read()
        with open(outputPath, "w") as output:
            
            startIndex = stopIndex = 0
            while startIndex != -1:

                startIndex = document.find("path d", startIndex)
                output.write(document[stopIndex : startIndex])
                if startIndex != -1:
                    stopIndex = document.find("\"", startIndex + 8)
                    value : str = document[startIndex + 8: stopIndex]

                    newValue = bisectPathD(value)

                    output.write("path d=\"" + newValue)

                    startIndex += 8
            output.write(document[-1])

    else:
        print(f"Could not find \"{file}\" in \"{in_dir}\"")

    return

in_dir : str = "input/"
out_dir : str = "output/"
loopfor : int = len(sys.argv)

if loopfor < 2:
    for img in glob.glob(str(in_dir + '*.svg')):
        print(f"FOR IMAGE: {img}")
        bisectSVG(img[len(in_dir):], in_dir, out_dir)
else:
    i : int = 1
    while i < loopfor:
        bisectSVG(sys.argv[i], in_dir, out_dir)
        i += 1
