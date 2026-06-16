"""
    svgUngrouper.py

    Takes attributes from the g element and applies it to all groups
    NOTE: This is a work in progress. Right now, this simply applies attributes to subelements
    NOTE: This assumes the svg document is well-formed with the least amount of whitespace used
"""

import os
from sys import argv
import re
import glob

def findFirstString(document: str, strings: list[str], start: int):
    if len(document) < 1:
        return -1
    if start == None:
        start = 0
    closestString: str = None
    closestIndex: int = -1
    for string in strings:
        index = document.find(string, start)
        #print(f"Found {string} at {index}")
        if (closestIndex == -1 or index < closestIndex) and index != -1:
            closestString = string
            closestIndex = index

    return closestIndex, closestString

def processElement(element: str):

    elementData = re.split(" ", element, 1)
    name = elementData[0]
    if len(elementData) > 1:
        attributeString = elementData[1]

        data:str = re.split("=\"|\" |\"", attributeString)

        attributes:list[str] = []
        values:list[str] = []

        i:int = 0
        while i < len(data) - 1:
            if data[i] not in attributes:
                attributes.append(data[i])
                values.append(data[i + 1])
                #print(f"{data[i]}=\"{data[i + 1]}\"")
            else:
                pass
                #print(f"skipped {data[i]}=\"{data[i + 1]}\"")
            i += 2

        return name, attributes, values
    return name, [], []

def ungroupSVG(file: str, in_dir: str, out_dir: str):
    inputPath = str(in_dir + file)
    outputPath = str(out_dir + file)

    if os.path.isfile(inputPath):
        with open(inputPath, "r") as input:
            document = input.read()
        with open(outputPath, "w") as output:

            startIndex = 0
            gElementAttributes:list[str] = [] # stack algorithm stuff
            while startIndex != -1:
                startIndex, thing = findFirstString(document, ["<g>", "<g ", "</g>", "<g/>", "</", "<!--" ,"<"], startIndex)
                #print(f"startIndex: {startIndex} thing {thing}")

                if startIndex != -1:
                    elementCloser = document.find(">", startIndex)

                    if thing == "<g>" or thing == "<g/>": #if thing in ["<g>", "<g/>"]: is not logically equivalent
                        startIndex += len(thing)
                        if thing == "<g>":
                            gElementAttributes.append("")

                    elif thing == "<g ":
                        emptyElementCheck = document.find("/>", startIndex) # check for empty g element, these are not important

                        if emptyElementCheck == -1 or elementCloser < emptyElementCheck:
                            gAttributes:str = document[startIndex + 3: elementCloser]
                            #print(f"gAttributes: {gAttributes}")

                            gElementAttributes.append(gAttributes)

                            startIndex += 2 + len(gAttributes)
                    elif thing == "<":
                        emptyElementCheck = document.find("/>", startIndex) # check for other empty element

                        if emptyElementCheck != -1 and (elementCloser == -1 or emptyElementCheck < elementCloser):
                            #print("empty element")
                            elementAttributes: str = document[startIndex + 1: emptyElementCheck]
                            output.write("<")
                            bigString: str = elementAttributes

                            j: int = len(gElementAttributes) - 1
                            while j >= 0:
                                bigString = bigString + gElementAttributes[j]
                                j -= 1
                            name, attributes, values = processElement(bigString)
                            #print(f"name {name} attributes {attributes} values {values}")

                            output.write(name)
                            for k in range(len(attributes)):
                                output.write(" " + attributes[k] + "=\"" + values[k] + "\"")

                            output.write("/>\n")

                            startIndex += 1 + len(elementAttributes)
                        else:
                            #print("not empty element")
                            elementAttributes: str = document[startIndex + 1: elementCloser]
                            output.write("<")
                            bigString: str = elementAttributes

                            j: int = len(gElementAttributes) - 1
                            while j >= 0:
                                bigString = bigString + gElementAttributes[j]
                                j -= 1
                            name, attributes, values = processElement(bigString)

                            output.write(name)
                            for k in range(len(attributes)):
                                output.write(" " + attributes[k] + "=\"" + values[k] + "\"")

                            output.write(">\n")

                            startIndex += 0 + len(elementAttributes)

                    elif thing == "</g>":
                        gElementAttributes.pop() # There can't be more end tags than start tags in valid, usable xml.
                        startIndex += 4

                    elif thing == "</":
                        elementName: str =  document[startIndex + 1: elementCloser]
                        output.write("<" + elementName + ">\n")

                        startIndex += 0 + len(elementName)

                    elif thing == "<!--":
                        startIndex += 6

                    else:
                        print("How did we get here?")
                        exit()

    else:
        print(f"Could not find \"{file}\" in \"{in_dir}\"")

# importlib execution
def main(*args):

    in_dir: str = args[0]
    out_dir: str = args[1]
    leng: int = len(args)

    if leng < 3:
        for img in glob.glob(str(in_dir + '*.svg')):
            ungroupSVG(img[len(in_dir):], in_dir, out_dir)
    else:
        i: int = 2
        while i < leng:
            ungroupSVG(args[i], in_dir, out_dir)
            i += 1

# regular execution
if __name__ == "__main__":

    in_dir: str = "input/"
    out_dir: str = "output/"
    loopfor: int = len(argv) - 1

    if loopfor < 1:
        for img in glob.glob(str(in_dir + '*.svg')):
            ungroupSVG(img[len(in_dir):], in_dir, out_dir)

    else:
        i: int = 1
        while i < loopfor + 1:
            ungroupSVG(argv[i], in_dir, out_dir)
            i += 1
