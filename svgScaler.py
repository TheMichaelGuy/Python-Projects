"""
    svgScaler.py

    Exports an svg document altered by a size multiplier
    This uses command line parameters argv[1] = multiplier, argv[2:] = files to edit
    This is also meant for certain svg sprites made in Scratch
"""

import os
import sys
import re

# https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/d
# https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/linearGradient

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

def findFirstString(document : str, strings : list[str], start : int): # this could definitely be optimized with a priority queue in the main program
    if len(document) < 1:
        return -1
    if start == None:
        start = 0
    closestString : str = None
    closestIndex : int = -1
    for string in strings:
        index = document.find(string, start)
        if (closestIndex == -1 or index < closestIndex) and index != -1:
            closestString = string
            closestIndex = index

    return closestIndex, closestString

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

def scalePathCommands(dPathCommands : list[list[str]], multiplier : float):
    if not dPathCommands:
        return ""
    # isolate all numbers
    dPathNumbers = []
    for pair in dPathCommands:
        dPathNumbers.append([pair[0], re.split(",| ", pair[1])])
    # apply multiplication to necessary numbers
    newStrings : list[str] = []
    for pair in dPathNumbers:
        if pair[0] in "MmLlTtCcSsHhVvQq": # Coordinate Variables
            parameterSet : str = ""
            delimiterBit : bool = False
            isFirst : bool = True
            for num in pair[1]:
                num = multiplier * float(num)
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
            pair[1][0] = multiplier * float(pair[1][0])
            pair[1][1] = multiplier * float(pair[1][1])
            pair[1][5] = multiplier * float(pair[1][5])
            pair[1][6] = multiplier * float(pair[1][6])
            newStrings.append(str(pair[0]) + " " + str(pair[1][0]) + " " + str(pair[1][1]) + " " + str(pair[1][2]) + " " + str(pair[1][3]) + " " + str(pair[1][4]) + " " + str(pair[1][5]) + "," + str(pair[1][6]))
        if pair[0] in "Zz": # 0 vars
            newStrings.append(str(pair[0]))

    # rejoin all strings appropriately
    finalString : str = ""
    for func in newStrings:
        finalString += func
    return finalString

def scaleValue(text : str, multiplier : float):
    return str(multiplier * float(text))

def scaleTranslate(text : str, multiplier : float):
    if text[0:10] != "translate(":
        return text
    pair = text[10:-1]
    v1, v2 = pair.split(",")
    v1 = multiplier * float(v1)
    v2 = multiplier * float(v2)
    return "translate(" + str(v1) + "," + str(v2) + ")"

def scaleViewBox(text: str, multiplier : float):
    box = text.split(",")
    newViewBox = ""
    isfirst = True
    for val in box:
        newViewBox += ("," if not isfirst else "") + scaleValue(val, multiplier)
        isfirst = False
    return newViewBox

def scalePathD(text : str, multiplier : float):
    return scalePathCommands(splitPathDCommands(text), multiplier)

in_dir : str = "input/"
out_dir : str = "output/"
loopfor : int = len(sys.argv) - 1

if loopfor < 1:
    print("No command line arguments")
    exit

multiplier = float(sys.argv[1])

i : int = 2
while i < loopfor + 1:
    inputPath = str(in_dir + sys.argv[i])
    outputPath = str(out_dir + sys.argv[i])

    if os.path.isfile(inputPath):
        with open(inputPath, "r") as input:
            document = input.read()
        with open(outputPath, "w") as output:

            startIndex = stopIndex = 0
            attributes : list[str] = ["width", "height", "viewBox", "x1", "y1", "x2", "y2", "g transform", "path d", "stroke-width"]
            while startIndex != -1:
                
                startIndex, result = findFirstString(document, attributes, startIndex)
                output.write(document[stopIndex : startIndex])
                if startIndex != -1:

                    stopIndex = document.find("\"", startIndex + len(result) + 2)
                    value : str = document[startIndex + len(result) + 2: stopIndex]
                    newValue : str
                    if(result in ["width", "height", "stroke-width", "x1", "y1", "x2", "y2"]):
                        newValue = scaleValue(value, multiplier)
                    elif(result == "viewBox"):
                        newValue = scaleViewBox(value, multiplier)
                    elif(result == "g transform"):
                        newValue = scaleTranslate(value, multiplier)
                    elif(result == "path d"):
                        newValue = scalePathD(value, multiplier)
                    output.write(result + ("=\"" if result != "linearGradient" else " ") + newValue)
                    startIndex += len(result) + 2
            output.write(document[-1])
    
    else:
        print(f"Could not find \"{sys.argv[i]}\" in \"{in_dir}\"")
    i += 1
