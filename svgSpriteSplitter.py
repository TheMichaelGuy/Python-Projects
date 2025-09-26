"""
    svgSpriteSplitter.svg

    Separates a Scratch SVG file into multiple files based on the grouping of sprite objects
    This program exists solely for files organized in a particular way and may not be well adapted for every SVG document
"""

import os
import sys
import re
import glob

class BaseFileInfo:

    header : str = "" # <svg ...
    encapsulatingGroups: list[str] = [] # all g elements that encompass the entire svg, should go on every file
    ungroupedData : list[str] = []
    comments : list[str] = []

class Collection:

    def __init__(self, g : str = "<g>", index : int = -1):
        self.groupHeader : str = g
        self.startIndex : int = index # Collected at the start of 'isCollecting'
    stopIndex : int = -1 # Collected at the end of 'isCollecting'

class DefsList:

    defEntry : list[str] = []
    defIDs : list[str] = []

def findAttribute(string : str, name : str, start : int):
    if len(string) < 1:
        return "", -1
    if start == None:
        start = 0
    namePos = string.find(str(name + "=\""), start)
    if namePos == -1:
        return "", -1
    startPos = namePos + len(name) + 2
    endPos = string.find("\"", startPos)
    if endPos == -1:
        return "", -1
    data = string[startPos:endPos]
    
    return data, namePos

def findFirstString(document : str, strings : list[str], start : int):
    if len(document) < 1:
        return -1
    if start == None:
        start = 0
    closestString : str = None
    closestIndex : int = -1
    for string in strings:
        index = document.find(string, start)
        ##print(f"Found {string} at {index}")
        if (closestIndex == -1 or index < closestIndex) and index != -1:
            closestString = string
            closestIndex = index

    return closestIndex, closestString

def processElement(element : str):

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
                ##print(f"{data[i]}=\"{data[i + 1]}\"")
            else:
                pass
                ##print(f"skipped {data[i]}=\"{data[i + 1]}\"")
            i += 2

        return name, attributes, values
    return name, [], []

def splitSprite(file: str, in_dir : str, out_dir : str):
    inputPath = str(in_dir + file)
    outputPath = str(out_dir + file)
    if os.path.isfile(inputPath):
        with open(inputPath, "r") as input:
            document = input.read()
        
            startIndex = 0 # reusing the same navigation as svgUngrouper.py

            isCollecting : bool = False # whether or not the program is actively getting info for a Collection entry
            isDefining : bool = True # the state before a collection has been detected

            gBaseLayer : int = 0 # keep track of how many groups exist before a group touches a non group element
            gCollectionLayer : int = 0 # keep track of what level we are in a group in order to exit collection mode
            gLayer : int = None # group layering when not in collection mode

            baseFile : BaseFileInfo = BaseFileInfo() # info necessary to create file 1
            separatedFiles : list[Collection] = [] # info necessary to create files 2 to n
            fileIndex : int = -1 # which additional file we are on
            definitions : DefsList = DefsList() # info necessary to create files that need a defs element

            while startIndex != -1:
                startIndex, thing = findFirstString(document, ["<g>", "<g ", "</g>", "<g/>", "</", "<!--" ,"<"], startIndex)
                #print(f"BIG LAP AROUND THE SPLITTER: startIndex {startIndex} thing {thing}\n")

                if startIndex != -1:
                    elementCloser = document.find(">", startIndex)

                    if thing == "<g>" or thing == "<g/>": #if thing in ["<g>", "<g/>"]: is not logically equivalent
                        startIndex += len(thing)
                        if thing == "<g>":
                            if isDefining:
                                #print("Go down a blank G layer")
                                gBaseLayer += 1
                                baseFile.encapsulatingGroups.append("<g>")

                            elif isCollecting:
                                #print("This collection has a blank G layer")
                                gCollectionLayer += 1

                            else:
                                gLayer += 1
                                #print("Add that blank g to ungrouped data")
                                baseFile.ungroupedData.append("<g>\n")          

                    elif thing == "<g ":

                        emptyElementCheck = document.find("/>", startIndex) # check for empty g element, these are not important
                        
                        if emptyElementCheck == -1 or elementCloser < emptyElementCheck:
                            gAttributes:str = document[startIndex + 3 : elementCloser]
                            ##print(f"gAttributes: {gAttributes}")
                            if isDefining:
                                #print("We have some interesting g stuff here")
                                gBaseLayer += 1
                                baseFile.encapsulatingGroups.append("<g " + gAttributes + ">")
                            elif isCollecting:
                                #print("This collection has a grouped object inside")
                                gCollectionLayer += 1
                            else:
                                #print("Unsure of what to do here. Probably should copy to base file")
                                gLayer += 1
                                baseFile.ungroupedData.append("<g " + gAttributes + ">\n")

                            startIndex += 2 + len(gAttributes)
                        else:
                            #print("What type of edge case is this?!")
                            raise

                    elif thing == "<":

                        # grab element data
                        emptyElementCheck = document.find("/>", startIndex) # check for other empty element
                        isEmptyElement : bool = bool(emptyElementCheck != -1 and (elementCloser == -1 or emptyElementCheck < elementCloser))
                        if isEmptyElement:
                            elementCloser = emptyElementCheck
                        elementAttributes : str = document[startIndex + 1: elementCloser]
                        name, attributes, values = processElement(elementAttributes)
                        #print(f"big string stuff: name ({name}) attributes {attributes} values {values}")
                        if isEmptyElement:
                            startIndex += 1
                        startIndex += len(elementAttributes)

                        # handle element data
                        if isDefining:
                            #find header
                            if (name == 'svg'):
                                #print("Define the svg!")
                                baseFile.header = "<" + elementAttributes + ">"
                                ##print(f"header: {baseFile.header}")
                            elif (name == 'defs'):
                                #print("Define the defs!")
                                #do a mini parser
                                #locate all defined elements and their ids
                                #split that into different def entries
                                #advance into main svg
                                stopIndex = document.find("</defs>", startIndex)
                                defStartIndex : int
                                defStopIndex: int
                                while startIndex != -1 and stopIndex != -1 and startIndex < stopIndex:

                                    startIndex, tag = findFirstString(document, ["</","<"], startIndex)
                                    emptyElementCheck = document.find("/>", startIndex)
                                    elementCloser = document.find(">", startIndex)
                                    id, idPos = findAttribute(document, "id", startIndex)
                                    
                                    ##print(f"startIndex {startIndex} stopIndex {stopIndex} tag {tag} eeC {emptyElementCheck} eClose {elementCloser} id {id} idPos {idPos}")
                                    if emptyElementCheck != 1 and emptyElementCheck < elementCloser:
                                        elementCloser = emptyElementCheck

                                    if startIndex == stopIndex:
                                        ##print(f"ids {definitions.defIDs}\n content {definitions.defEntry}")
                                        #end of defs proper
                                        pass
                                    elif elementCloser < emptyElementCheck:
                                        if tag == "<":
                                            #startdefentry
                                            definitions.defIDs.append(id)
                                            defStartIndex = startIndex
                                        else: # tag == "</"
                                            definitions.defEntry.append(document[defStartIndex : elementCloser + 1])
                                            #enddefentry
                                    
                                    #otherwise, doesn't matter
                                    startIndex = elementCloser

                                startIndex = stopIndex + 7

                            else:
                                #print(f"Enter isCollectingMode baseLayer {gBaseLayer}")
                                isCollecting = True
                                isDefining = False
                                gCollectionLayer = 0
                                gLayer = gBaseLayer
                                
                                separatedFiles.append(Collection(baseFile.encapsulatingGroups.pop(), startIndex - len(elementAttributes) - (1 if isEmptyElement else 0)))
                            
                        elif isCollecting:
                            #print("pass though and increment")
                            pass
                        else:
                            if (gLayer == gBaseLayer):
                                #print(f"Reenter isCollectingMode baseLayer {gBaseLayer}")
                                isCollecting = True
                                gCollectionLayer = 0

                                separatedFiles.append(Collection(baseFile.ungroupedData.pop(), startIndex - len(elementAttributes) - (1 if isEmptyElement else 0)))

                            else:
                                #print("pass through and copy ungrouped data")
                                baseFile.ungroupedData.append("<" + elementAttributes + ("/>" if isEmptyElement else ">"))

                                # This is for that tspan edge case that could apply to a slim amount of other attribites
                                if not isEmptyElement and (document.find(">" ,startIndex) != -1 and document.find("<" ,startIndex) != -1) and (document.find("<" ,startIndex) - document.find(">" ,startIndex) > 1):
                                    #print("THE TSPAN! THE TSPAN IS REAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAL!")
                                    baseFile.ungroupedData.append(document[document.find(">" ,startIndex) + 1 : document.find("<" ,startIndex)])

                    elif thing == "</g>":
                        if isDefining:
                            #print("unpeeling before collection?!")
                            raise
                        elif isCollecting:
                            #print("unpeeling one layer")
                            gCollectionLayer -= 1
                            if gCollectionLayer < 0:
                                #print("exiting isCollecting")
                                isCollecting = False
                                gLayer -= 1
                                separatedFiles[-1].stopIndex = startIndex
                        else:
                            #print("unpeeling after atleast one collection")
                            baseFile.ungroupedData.append("</g>")
                            gLayer -= 1
  
                        #gElementAttributes.pop() # There can't be more end tags than start tags in valid, usable xml.
                        startIndex += 4

                    elif thing == "</":
                        elementName : str =  document[startIndex + 1: elementCloser]
                        #print(f"closing {elementName}")
                        #output.write("<" + elementName + ">\n")
                        if not (isDefining or isCollecting):
                            baseFile.ungroupedData.append("<" + elementName + ">")
                        startIndex += 0 + len(elementName)

                    elif thing == "<!--":
                        #print("We'll need to copy this comment")
                        commentCloser = document.find("-->", startIndex)
                        baseFile.comments.append("<!--" + document[startIndex + 4 : commentCloser] + "-->")
                        startIndex += 6

                    else:
                        #print("How did we get here?")
                        exit

        #print("Then, this is where we'd do the file writing")

        ##print("BASE FILE INFO")
        ##print(f"header {baseFile.header}")
        #for group in baseFile.encapsulatingGroups:
        #    #print(f"group: {group}")
        #    pass
        ##print("other info")
        #for other in baseFile.ungroupedData:
        #    #print(other)
        #    pass
        #for comment in baseFile.comments:
        #    #print(comment)
        #    pass
        #
        ##print("COLLECTIONS")
        #for collection in separatedFiles:
        #    #print(f"Isolate this!")
        #    #print(f"g = {collection.groupHeader}")
        #    #print(f"starts at {collection.startIndex} and ends at {collection.stopIndex}")
        #    pass
        #
        ##print("DEFS")
        ##print(definitions.defEntry)

        myDefs : list[str] = []
        for defs in range(len(definitions.defIDs)):
            for line in baseFile.ungroupedData:
                if line.find("url(#" + definitions.defIDs[defs] + ")") != -1:
                    myDefs.append(definitions.defEntry[defs])

        with open(str(outputPath[:-4] + "-1" + ".svg"), "w") as output:
            output.write(baseFile.header)
            if len(myDefs) > 0:
                output.write("<defs>")
                for defs in myDefs:
                    output.write(defs)
                output.write("</defs>")
            for group in baseFile.encapsulatingGroups:
                output.write(group)
            for other in baseFile.ungroupedData:
                output.write(other)
            for comment in baseFile.comments:
                output.write(comment)
    
        counter : int = 1
        for collection in separatedFiles:
            counter += 1
            someDefs : list[str] = []
            content : str = document[collection.startIndex : collection.stopIndex]
            for defs in range(len(definitions.defIDs)):
                #print(definitions.defIDs[defs])
                if content.find("url(#" + definitions.defIDs[defs] + ")") != -1:
                    someDefs.append(definitions.defEntry[defs])
            with open(str(outputPath[:-4] + "-" + str(counter) + ".svg"), "w") as output:
                output.write(baseFile.header)
                if len(someDefs) > 0:
                    output.write("<defs>")
                    for defs in someDefs:
                        output.write(defs)
                    output.write("</defs>")
                for group in baseFile.encapsulatingGroups:
                    output.write(group)
                output.write(collection.groupHeader)
                output.write(content)
                for _ in range(len(baseFile.encapsulatingGroups) + 1):
                    output.write("</g>")
                output.write("</svg>")

    else:
        print(f"Could not find \"{file}\" in \"{in_dir}\"")

    return

in_dir : str = "input/"
out_dir : str = "output/"
loopfor : int = len(sys.argv) - 1

if loopfor < 1:
    answer = input("You entered no command line arguments. If you continue, svgSpriteSplitter.svg will run on all of your SVGs which may take a lot of time or space. Enter 'Y' to proceed or anything else to exit: ")
    if answer == 'Y':
        print("Continuing...")
        for img in glob.glob(str(in_dir + '*.svg')):
            splitSprite(img[len(in_dir):], in_dir, out_dir)
        print("Complete!")
    else:
        print("Successfully Cancelled.")
else:
    i : int = 1
    while i < loopfor + 1:
        splitSprite(sys.argv[i], in_dir, out_dir)
        i += 1
